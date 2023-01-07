import os
from _curses import error
from datetime import datetime

from gmailconnector.validator import validate_email
from pick import pick

date = datetime.now().strftime("%B %d %Y %I:%M %p")

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

default_id = os.environ.get('recipient')
prompt = f'Enter the email address:'

if default_id:
    prompt += "\t(Hit return to default to {default_id})\n"
else:
    prompt += "\n"


def get_target():
    get_target.count += 1
    if addr := input(prompt):
        return addr
    elif default_id:
        return default_id
    else:
        if get_target.count > 2:
            raise SystemExit("Cannot proceed without a destination email address.")
        get_target()


get_target.count = 0
target = get_target()
result = validate_email(email_address=target, smtp_check=False)
if result.ok is False:
    raise SystemExit(result.body)

default_sub = f"Test email from {os.environ.get('USER')} at {date}"
sub = input(f'Enter the subject of the email:\t(Hit return to default to {default_sub!r})\n')
if not sub:
    sub = default_sub

body = input('Enter body of the email:\n') or ""
attachment = input('Enter the name of path of the attachment file:\t(Hit return for None)\n')
cmd = None
if attachment and not os.path.isfile(attachment):
    os.system(f'echo "Skipping attachment as {attachment} is not available at {os.getcwd()}"\n')
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
    if attachment.endswith('.html') and os.path.isfile(attachment):
        if not index:
            cmd = f"echo '{body}' | mail -s '{sub}' --alternative --content-type=text/html --attach={attachment} {target}"  # noqa
        else:
            cmd = f"echo '{body}' | mail -s '{sub}' --content-type=text/html --attach={attachment} {target}"
    elif os.path.isfile(attachment):
        if not index:
            cmd = f"echo '{body}' | mail -s '{sub}' --alternative --content-type=text/plain --attach={attachment} {target}"  # noqa
        else:
            cmd = f"echo '{body}' | mail -s '{sub}' --content-type=text/plain --attach={attachment} {target}"

if not cmd:
    cmd = f"echo '{body}' | mail -s '{sub}' {target}"

response = os.system(cmd)

if response == 0:
    print(f'Email has been sent to {target}.')
else:
    print('Email Undelivered.' + '\n' + str(response))
