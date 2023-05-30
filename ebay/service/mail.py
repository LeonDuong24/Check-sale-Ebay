import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Mail():
    def __init__(self,subject,html,receiver_email):
        super().__init__()
        self.email_address = "thongnhat91.hvn@gmail.com"
        self.email_password = "rjjvdcwnzytrsirm"
        self.receiver_email = receiver_email
        self.html_content=html
        self.subject=subject    
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
      
        
# message["Subject"] = "CID image test"
# message["From"] = from_email
# message["To"] = receiver_email

# # write the HTML part
# html = """\
# <html>
#  <body>
#    <img src="cid:Mailtrapimage">
#  </body>
# </html>
# """

# part = MIMEText(html, "html")
# message.attach(part)
# # msg.attach(MIMEText(message, "plain"))
# # # We assume that the image file is in the same directory that you run your Python script from
# # FP = open('mailtrap.jpg', 'rb')
# # image = MIMEImage(fp.read())
# # fp.close()

# # # Specify the  ID according to the img src in the HTML part
# # image.add_header('Content-ID', '<Mailtrapimage>')
# # message.attach(image)

# # send your email
# with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
#     smtp.starttls()
#     smtp.login(email_address, email_password)
#     smtp.send_message(message)