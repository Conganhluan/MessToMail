import os
import sys
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as BS

MAX_RETRIES = 5
#sys.stderr = open("/dev/null", "w")

#Functions used for debugging
def printContent(string):
    page = BS(string, "xml")
    original_stdout = sys.stdout
    with open("index.html","w") as file:
        sys.stdout = file
        print(page)
        sys.stdout = original_stdout
        file.close()

def printJson(json_obj):
    json_string = json.dumps(json_obj, indent=4)
    file = open("response.json", "w")
    file.write(json_string)
    file.close()

#Fucntion to get json object
def getJson(path):
    file = open(os.path.join(os.path.dirname(__file__), path), "r")
    json_obj = json.load(file)
    file.close()
    return json_obj

#Load the personal information
information = getJson(sys.argv[1])[0]
bkel_username = information["bkel_username"]
bkel_password = information["bkel_password"]
email_sender = information["email_sender"]
email_receiver = information["email_receiver"]
webmail_host = information["webmail_host"]
SMTP_user = information["SMTP_user"]
SMTP_password = information["SMTP_password"]
save_path = information["save_path"]
use_option = information["use_option"]

#Pre-check for the program
if (use_option!=1 and use_option!=2 and use_option!=3):
    print("The option number is wrong, please read README.md and modify the personal_information.json properly!")
    quit()

#URL for authentication
url1 = "https://sso.hcmut.edu.vn/cas/login?service=https://e-learning.hcmut.edu.vn/login/index.php?authCAS=CAS"
#URL for getting sesskey and userid
url2 = "https://e-learning.hcmut.edu.vn/message/index.php"

#Start the session
session = requests.Session()
#session.verify = False                                                         #if there is error about SSLAuthentication, un-commment this line

#Phase 1 - Get the needed cookies for the authentication pages

for retry in range(MAX_RETRIES): 
    response = session.get(url1)
    if response.ok:
        break
    else:
        print("Connect failed with the url!" + response.url)
        attempts_left = MAX_RETRIES - retry - 1
        if (attempts_left != 0):
            print(str(attempts_left) + " attempts left!")
        else: 
            print("Stop the program!")
            quit()

data = {
    "username" : bkel_username,
    "password" : bkel_password
}
finder = BS(response.content,"lxml")
foundList = finder.find_all("input")
for i in range(3, 7):                                                           #if the web is updated, this code (range(3,7)) may create bugs
    hiddenData = foundList[i]
    data[hiddenData.attrs["name"]] = hiddenData.attrs["value"]

#Phase 2 - Bypass the authentication with username and password (and hidden tickets, etc.)

for retry in range(MAX_RETRIES):
    response = session.post(url1, data=data)
    if response.ok:
        break
    else:
        print("Connect failed with the url!" + response.url)
        attempts_left = MAX_RETRIES - retry - 1
        if (attempts_left != 0):
            print(str(attempts_left) + " attempts left!")
        else: 
            print("Stop the program!")
            quit()

    #Navigate to messages page
for retry in range(MAX_RETRIES):
    response = session.get(url2)
    if response.ok:
        break
    else:
        print("Connect failed with the url!" + response.url)
        attempts_left = MAX_RETRIES - retry - 1
        if (attempts_left != 0):
            print(str(attempts_left) + " attempts left!")
        else: 
            print("Stop the program!")
            quit()

    #Get the sesskey for the url
finder = BS(response.content,"lxml")
json_url = finder.find_all("a")[22].attrs["href"].replace("https://e-learning.hcmut.edu.vn/login/logout.php?sesskey=", "https://e-learning.hcmut.edu.vn/lib/ajax/service.php?sesskey=") + "&info=core_message_get_conversation_counts,core_message_get_unread_conversation_counts"
                                                                                #if the web is updated, this code (22) may create bugs
    #Get the userid for the data
userid = finder.find_all("div")[12].attrs["data-userid"]                        #if the web is updated, this code (12) may create bugs

    #Load the json prepared for the request
json_obj = getJson("get_unread_chats_count.json")
json_obj[0]["args"]["userid"] = userid
json_obj[1]["args"]["userid"] = userid

    #Check if there are unread messages
for retry in range(MAX_RETRIES):
    response = session.post(json_url, json=json_obj, headers={"Accept": "application/json"})
    if response.ok:
        break
    else:
        print("Connect failed with the url!" + response.url)
        attempts_left = MAX_RETRIES - retry - 1
        if (attempts_left != 0):
            print((attempts_left) + " attempts left!")
        else: 
            print("Stop the program!")
            quit()

json_response = response.json()
num_of_unread_chat = json_response[1]["data"]["types"]["1"]
num_of_total_chat = json_response[0]["data"]["types"]["1"]

if num_of_unread_chat == 0:
    sys.exit("There is none of unread messages")
else:
    print("There are " + str(num_of_unread_chat) + " unread chats")

#Phase 3 - Get the unread messages

    #Load the json prepared for the request
json_obj = getJson("get_unread_chats.json")
json_obj[0]["args"]["userid"] = userid

    #Update the url and get id, and number of unread messages of the unread chats
json_url = json_url.replace("core_message_get_conversation_counts,core_message_get_unread_conversation_counts", "core_message_get_conversations")

for retry in range(MAX_RETRIES):
    response = session.post(json_url, json=json_obj, headers={"Accept": "application/json"})
    if response.ok:
        break
    else:
        print("Connect failed with the url!" + response.url)
        attempts_left = MAX_RETRIES - retry - 1
        if (attempts_left != 0):
            print(str(attempts_left) + " attempts left!")
        else: 
            print("Stop the program!")
            quit()

json_response = response.json()

id_unread_chats = []
num_unread_messages = []
messages = {}
for i in range(0, num_of_total_chat):
    chat = json_response[0]["data"]["conversations"][i]
    if (chat["unreadcount"] != None):
        id_unread_chats.append(chat["id"])
        num_unread_messages.append(chat["unreadcount"])

    #Load the json prepared for the request
json_obj = getJson("get_messages.json")
json_obj[0]["args"]["currentuserid"] = int(userid)

    #Update url and get unread messages
json_url = json_url.replace("core_message_get_conversations", "core_message_get_conversation_messages")

    #For each unread chat
for i in range(0, num_of_unread_chat):
    json_obj[0]["args"]["convid"] = int(id_unread_chats[i])
    json_obj[0]["args"]["limitnum"] = int(num_unread_messages[i])
    
    for retry in range(MAX_RETRIES):
        response = session.post(json_url, json=json_obj, headers={"Accept": "application/json"})
        if response.ok:
            break
        else:
            print("Connect failed with the url!" + response.url)
            attempts_left = MAX_RETRIES - retry - 1
            if (attempts_left != 0):
                print(str(attempts_left) + " attempts left!")
            else: 
                print("Stop the program!")
                quit()
    
    json_response = response.json()
    author = json_response[0]["data"]["members"][0]["fullname"]
    messages[author] = []

        #For each unread messages in that chat
    for j in range(0, num_unread_messages[i]):
        message = json_response[0]["data"]["messages"][j]["text"]
        messages[author].append(message)

#Phase 4 - Mark messages all read and log out
'''
    #Load the json prepared for the request
json_obj = getJson("mark_messages_read.json")
json_obj[0]["args"]["userid"] = int(userid)

    #Update url and mark all messages as read
json_url = json_url.replace("core_message_get_conversation_messages", "core_message_mark_all_conversation_messages_as_read")
for i in range(0, num_of_unread_chat):
    json_obj[0]["args"]["conversationid"] = int(id_unread_chats[i])
    
    for retry in range(MAX_RETRIES):
        response = session.post(json_url, json=json_obj, headers={"Accept": "application/json"})
        if response.ok:
            break
        else:
            print("Connect failed with the url!" + response.url)
            attempts_left = MAX_RETRIES - retry - 1
            if (attempts_left != 0):
                print(str(attempts_left) + " attempts left!")
            else: 
                print("Stop the program!")
                quit()
    
    json_response = response.json()
'''
session.close()

#Phase 5 - Send the emails/ Save into the files

    #Send the emails
if use_option == 1 or use_option == 3:
    for i in messages:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = i + " has sent from the Bkel"
        msg['From'] = email_sender
        msg['To'] = email_receiver
        for j in messages[i]:
            body = MIMEText(j, 'html', "UTF-8")
            msg.attach(body)
            s = smtplib.SMTP(webmail_host)
            #s.login(SMTP_user, SMTP_password)
            s.sendmail(email_sender, email_receiver, msg.as_string())
            s.quit()

    #Save into the files
if use_option == 2 or use_option == 3:
    save_path = save_path + "Messages"
    if os.path.exists(save_path) == False:
        os.mkdir(save_path)

    for i in messages:
        for j in messages[i]:
            file = open(os.path.join(save_path, i + ".html"), mode="a", encoding="UTF-8")
            file.write(j)
            file.close()

sys.stderr.close()