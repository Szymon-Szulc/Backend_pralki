import json
import os
import random
from smtplib import SMTP_SSL

from redmail import EmailSender

from .common import get_dev

json_path = "json/mail/"


class Mail:
    @staticmethod
    def send(to_email, key_mail, args1, args2, lang='pl'):
        email = EmailSender(host="ssl0.ovh.net", port=465, cls_smtp=SMTP_SSL, username=os.environ.get("MAIL_USERNAME"),
                            password=os.environ.get("MAIL_PASSWORD"), use_starttls=False)
        with open('{0}{1}.json'.format(json_path, lang), encoding="UTF-8") as f:
            data = json.load(f)
        subject = data[key_mail]['title']
        html_body = data[key_mail]['msg'].format(args1, args2)
        email.send(
            subject=subject,
            sender=os.environ.get("MAIL_USERNAME"),
            receivers=[to_email],
            text="",
            html=html_body
        )

    @staticmethod
    def code_gen(length=5):
        dev = get_dev()
        code = ""
        if dev == "True" or dev is True:
            return "11111"
        for i in range(length):
            code += str(random.choice(range(0, 9)))
        return code
