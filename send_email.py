from _curses import error
from datetime import datetime
from os import environ, getcwd, path, system
from re import match

from pick import pick

date = datetime.now().strftime("%B %d %Y %I:%M %p")

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

default_id = environ.get('recipient')
target = input(f'Enter the email address:\t(Hit return to default to {default_id})\n')

if not target:
    target = default_id


def check(email):
    if not (match(regex, email)):
        return False
    return True


if not target:
    exit('Recipient email address is mandatory!!!')

if not check(email=target):
    exit('Invalid email address received.')

default_sub = f"This is the subject line sent at {date}"
sub = input(f'Enter the subject of the email:\t(Hit return to default to {default_sub})\n')
if not sub:
    sub = default_sub

body = input('Enter body of the email:\n')
if not body:
    body = ""

attachment = input('Enter the name of the attachment file:\t(Hit return for None)\n')

cmd = None
if attachment and not path.isfile(attachment):
    system(f'echo "Skipping attachment as {attachment} is not available at {getcwd()}"\n')
elif attachment:
    title = "Please pick an attachment type: "
    options = [
        'Inlined attachment\tNote: Inlined attachments may end up in spam folder if they display a potential threat',
        'File attachment'
    ]
    try:
        option, index = pick(options, title, indicator='=>', default_index=0)
    except error:
        index = 1
    if attachment.endswith('.html') and path.isfile(attachment):
        if not index:
            cmd = f"echo '{body}' | mail -s '{sub}' --alternative --content-type=text/html --attach={attachment} {target}"  # noqa
        else:
            cmd = f"echo '{body}' | mail -s '{sub}' --content-type=text/html --attach={attachment} {target}"
    elif path.isfile(attachment):
        if not index:
            cmd = f"echo '{body}' | mail -s '{sub}' --alternative --content-type=text/plain --attach={attachment} {target}"  # noqa
        else:
            cmd = f"echo '{body}' | mail -s '{sub}' --content-type=text/plain --attach={attachment} {target}"

if not cmd:
    cmd = f"echo '{body}' | mail -s '{sub}' {target}"

response = system(cmd)

if response == 0:
    print(f'Email has been sent to {target}.')
else:
    print('Email Undelivered.' + '\n' + str(response))
