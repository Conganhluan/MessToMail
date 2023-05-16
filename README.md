# MESSAGE TO MAIL
Đây là một chương trình phục vụ cho mục đích cá nhân chính là có thể chuyển những tin nhắn trên Bkel - trang web dùng để trao đổi của những giảng viên và sinh viên thuộc trường Đại học Bách Khoa - ĐHQG-HCM - thành những email và gửi về trực tiếp đến gmail cá nhân của mình.  
Mã nguồn đã được viết theo hướng phù hợp cho tất cả người dùng nếu có nhu cầu giống mình; nhưng tất nhiên sẽ có vài điểm cần chỉnh sửa để phù hợp với từng người, mình sẽ đề cập rõ hơn bên dưới.  
    
This is a program created for personal purpose, which is to convert the messages on Bkel - the website used for interactions between every teachers and students in HCM city University of Technology - into emails and send them directly to my personal email.  
The source code was designed to be suitable for anyone whose need is like me; but of course, there will be some elements which need personalizing to fit the user, I will go into details below.  
  
## Điều kiện tiên quyết/ Presiquites:
Để chạy được các code này, máy tính cần có Python. Ngoài các thư viện đã có sẵn, bạn cũng cần phải cài đặt những thư viện riêng mà chương trình đã sử dụng bao gồm `requests`, `emails`, `beautifulsoup4` nếu máy bạn chưa có. 
Theo mặc định, chương trình sẽ sử dụng *localhost* cho SMTP (dịch vụ gửi thư), vậy nên máy tính của bạn cần phải được cài đặt dịch vụ SMTP trước, hoặc bạn có thể chọn lưu thành các tệp tin thay vì gửi mail để không cần phải cài đặt SMTP. Nếu bạn sử dụng dịch vụ SMTP của các trang web thì bạn phải mở khóa dòng 163 `s.login(SMTP_user, SMTP_password)` để có thể đăng nhập vào dịch vụ đó.  
  
To run the code, the computer needs Python. Beside in-built libraries, you also need to install specially needed libariries for the program such as `requests`, `emails`, `beautifulsoup4` if the computer doesn't have them yet.  
By default, the program will use *localhost* for STMP (email service) so that your computer needs to install the SMTP in advance, unless you prefer saving messages into files instead of sending emails. If you use SMTP service on another host then you have to un-comment the code in line 163 `s.login(SMTP_user, SMTP_password)` which allows you to login those web services.  
  
## Cách cài đặt và sử dụng/ How to install and use:
Để cài đặt, các bạn tải (hoặc nhân bản) mã nguồn về, sau đó điền đầy đủ các thông tin cá nhân vào tệp tin *personal_information.json* như sau:  
- **email_sender**: Email dùng để gửi mail
- **email_receiver**: Email dùng để nhận mail và thông báo cho bạn biết
- **bkel_username**: Tên tài khoản dùng để đăng nhập vào *Dịch vụ xác thực tập trung của BKEL*
- **bkel_password**: Mật khẩu của tài khoản dùng để đăng nhập vào *Dịch vụ xác thực tập trung của BKEL*
- **webmail_host** : Máy chủ dùng để sử dụng dịch vụ SMTP (mặc định là *localhost*)
- **SMTP_user**: Tên tài khoản dùng để đăng nhập vào dịch vụ SMTP, thường là **email_sender**
- **SMTP_password**: Mật khẩu của tài khoản dùng để đăng nhập vào dịch vụ SMTP
- **save_path**: Đường dẫn để thư mục lưu những tệp tin chứa nội dung tin nhắn. Ví dụ: "C:/Users/Desktop/", khi chạy thì chương trình sẽ tạo thư mục *Messages* trong đường dẫn đã thiết lập và tiến hành lưu các tệp tin vào đấy.
- **use_option** : Bao gồm những lựa chọn sau đây:
    - 1: Chuyển các tin nhắn thành mail và chuyển đến hộp thư điện tử như đã thiết lập
    - 2: Chuyển các tin nhắn thành các tệp tin và lưu vào nơi đã được chỉ định
    - 3: Thực hiện cả hai hành động trên
  
Để khởi chạy chương trình, bạn chỉ cần gọi lệnh `python /path/to/main.py` là hoàn thành. Để chương trình đạt được hiệu quả tốt nhất, bạn nên sử dụng một phần mềm khác để lên lịch thực hiện nó theo định kì. Nếu bạn chạy trên hosting của chính mình và gặp lỗi thì có thể mở khóa câu lệnh ở dòng 57 `#session.verify = False` để sửa lỗi. Mọi lỗi khác nếu có xin vui lòng liên hệ với mình để mình có thể sửa chữa một cách sớm nhất!  
  
To install, you download (or clone) the source code, then fill completely your personal settings into the file *personal_information.json* including:  
- **email_sender**: The email used to send mails
- **email_receiver**: The email used to receive mails and notify you
- **bkel_username**: The account's username to log in the *Central Authentication Service for BKEL*
- **bkel_password**: The account's password to log in the *Central Authentication Service for BKEL*
- **webmail_host** :The host used to provide the SMTP service (mặc định là *localhost*)
- **SMTP_user**: The email used to log in the SMTP service, normally **email_sender**
- **SMTP_password**: The password along with email used to log in the SMTP service
- **save_path**: The path to the directory storing messages. For example: "C:/Users/Desktop/"; when running, the program creates a directory *Messages* in the chosen path and save files in there.
- **use_option** : There are options:
    - 1: Convert the messages into mails and send them to the chosen email
    - 2: Convert the messages into .html files and save them in the chosen path
    - 3: Do both
  
To run the program, you will run `python /path/to/main.py` and it's done. For the most effciency, you should use another programs for scheduling this program to run periodically. If you run this program on your own hosting and encounter error, you may un-commment `#session.verify = False` to fix it. Please let me know when you encounter a bug, I will fix and update the program as soon as possible!  
  
## Nguồn tham khảo/ References
Mình xin gửi lời cảm ơn chân thành đến những người lạ mà mình chưa quen biết, nhưng lại giúp đỡ mình rất nhiều trên các diễn đàn khi mình đang bước trên con đường của sự đau khổ và tuyệt vọng. Cụ thể hơn, những trang web mình đã học tập, tham khảo, cũng như tham gia vào các cuộc hỏi đáp hữu ích từ những người đi trước sẽ được mình để ở bài viết của mình https://conganhluan.com/personal-blog/hcmut-student/how-i-created-the-tool-mess-to-mail/, các bạn hãy đón xem nha!  
  
I would love to say sincerely "thank you" to those all strangers, whom I have ever known, but have helped me a lot on the forums when I am feeling depressed and painful. For more detail, the websites that I have learned, referenced, and taken part in extremely useful Q&As from predecessors will be revealed on the post https://conganhluan.com/personal-blog/hcmut-student/how-i-created-the-tool-mess-to-mail/, looking forward to seeing you there!
