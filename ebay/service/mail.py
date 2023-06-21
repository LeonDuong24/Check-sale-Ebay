import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from service.decorate import retry
class Mail():
    def __init__(self,subject,html,receiver_email):
        super().__init__()
        self.email_address = "tranhuulocnapa@gmail.com"#"thongnhat91.hvn@gmail.com"
        self.email_password = "guoknxmowhvhyldn"#"rjjvdcwnzytrsirm"
        self.receiver_email = receiver_email
        self.html_content=html
        self.subject=subject
        
    #@retry(max_attempts=5,retry_interval=10)    
    def send(self):
      message = MIMEMultipart("alternative")
      message["Subject"] = self.subject
      message["From"] = self.email_address
      message["To"] = self.receiver_email
      part = MIMEText(self.html_content, "html")
      message.attach(part)
      with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
          smtp.starttls()
          smtp.login(self.email_address, self.email_password)
          smtp.send_message(message)
      