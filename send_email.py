from datetime import datetime
from os import system, environ
from platform import system as os

if os() != 'Linux':
    exit('mailutils can only run on linux machines.')

date = datetime.now().strftime("%B %d %Y %I:%M %p")

default_id = environ.get('recipient')
target = input(f'Enter the email address:\t(Hit return to default to {default_id})\n')

if not target:
    target = default_id

if not target:
    exit('Recipient email address is mandatory!!!')

default_sub = f"This is the subject line sent at {date}"
subject = input(f'Enter the subject of the email:\t(Hit return to default to {default_sub})\n')
if not subject:
    subject = default_sub

body = input('Enter body of the email:\n')
if not body:
    body = ""

cmd = f"echo '{body}' | mail -s '{subject}' {target}"  # This is the only command we care about
response = system(cmd)

if response == 0:
    print('Email has been delivered.')
else:
    print('Email Undelivered.' + '\n' + str(response))
