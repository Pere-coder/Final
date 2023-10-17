from celery import shared_task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages

@shared_task
def send_emails_task(sender_email, sender_password, email_data):
        try:
            with open("./app/templates/config.txt", "r") as config_file:
                subject = config_file.read().strip()
            
            with open('./app/templates/C.txt', 'r') as body_file:
                email_body = body_file.read()
            
            for data in email_data:
                lines = data.split('\n')
                sender_name = lines[0].strip()
                recipient_info = lines[1].strip().split()
            
                # Extract recipient first name, full name, and email
                if len(recipient_info) >= 3:
                    recipient_firstname = recipient_info[0]
                    recipient_fullname = " ".join(recipient_info[:-1])
                    recipient_email = recipient_info[-1]
                else:
                    # Handle the case where recipient data is incomplete
                    recipient_firstname = ""
                    recipient_fullname = ""
                    recipient_email = ""
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                
                message = MIMEMultipart()
                message['From'] = f'{sender_name} <{sender_email}>'
                message['To'] = f'{recipient_fullname} <{recipient_email}>'
                message['Subject'] = subject

                # Email body
                email_text = f'Hello {recipient_firstname},\n\n{email_body}'
                message.attach(MIMEText(email_text, 'plain'))

                server.sendmail(sender_email, recipient_email, message.as_string())
                server.quit()
                print(f'Email sent successfully to {recipient_fullname}!')
        except Exception as e:
            print('Email sending failed', str(e))
        





