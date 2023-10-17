from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .tasks import send_emails_task
from django.core.files.storage import default_storage, FileSystemStorage
import os

def send_mail(request):
    if request.method == 'POST' and  'myfile' in request.FILES:
        sender_email = request.POST.get('sender_email')
        sender_password = request.POST.get('sender_password')
        myfile = request.FILES['myfile']
        
        folder = './app/templates/uploads'
        
        try:
            fs = FileSystemStorage(location=folder)
            filename = fs.save(myfile.name, myfile)
            if fs.exists(filename):
                print('success file')
            else:
                print('failed')
        except Exception as e:
            print(f'An error occured: {str(e)}')
        
        recent_file = get_most_recent_file(folder)
        
        if recent_file:
            with open(recent_file, "r") as file_b:
                email_data = file_b.read().strip().split('\n\n')
        else:
            print('No recent files found')
            
            
            
                
        email_data = email_data
        
        
        sender_e = sender_email
        sender_p= sender_password
        send_emails_task.delay(sender_e, sender_p, email_data)
        messages.success(request, "Emails succesfully scheduled. please view termnal to track emails")
        return redirect('/')
    return render(request, 'index.html')


def get_most_recent_file(folder):
    try:
        # List all files in the directory
        files = os.listdir(folder)
        if not files:
            return None

        # Sort files by modification time (most recent first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)

        # Get the most recent file
        most_recent_file = os.path.join(folder, files[0])
        return most_recent_file
    except Exception as e:
        print(f'Error while finding the most recent file: {str(e)}')
        return None
        
        