import os
import smtplib
#from google.appengine.ext.webapp import template
#from google.appengine.api import mail

from jinja2 import Template

Company_email = "Company Technologies <info@Company.com>"
john_email = "John <john@Company.com>"

sender_address = 'Company'
sender_pwd = "W1llR0bins0n!"

from_address = Company_email

to_user_subject = "Company registration confirmation"
to_Company_subject = "New user registration information"

_DEBUG = True

def send_email(user_address, subject, body_template, body_values):
    "Send email with Python's smtplib from webfaction"
    try:
        # Html email template
        mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.html')
        template = Template(open(mail_template).read())
        html_body = template.render(**body_values)

        msg = "To: %(contactEmail)s\r\nFrom: %(senderEmail)s\r\nSubject: %(subject)s\r\nContent-type: text/html\r\n\r\n%(body)s"
        msg = msg % {'contactEmail':user_address, 'senderEmail':from_address, 'subject':subject,'body':html_body}

        s = smtplib.SMTP()
        s.connect('smtp.webfaction.com')
        s.login(sender_address, sender_pwd)
        s.sendmail(from_address, user_address, msg)
    except Exception as e:
        print("Exception:", e)


def send_email_gmail(user_address, subject, body_template, body_values):
    "Send email with Python's smtplib"
    try:
        # Html email template
        mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.html')
        template = Template(open(mail_template).read())
        html_body = template.render(**body_values)

        msg = "To: %(contactEmail)s\r\nFrom: %(senderEmail)s\r\nSubject: %(subject)s\r\nContent-type: text/html\r\n\r\n%(body)s"
        msg = msg % {'contactEmail':user_address, 'senderEmail':sender_address, 'subject':subject,'body':html_body}

        server = smtplib.SMTP()
        server.connect('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_address, sender_pwd)
        server.sendmail(sender_address, user_address, msg)
        server.quit()
    except Exception as e:
        print("Exception:", e)

def send_email_appengine(sender_address, user_address, subject, body_template, body_values):
    if mail.is_email_valid(user_address):
        # Html email template
        mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.html')
        html_body = template.render(mail_template, body_values, debug=_DEBUG)
        # Text email template
        mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.txt')
        txt_body = template.render(mail_template, body_values, debug=_DEBUG)
        # Compose email
        message = mail.EmailMessage(sender=sender_address, subject=subject)
        message.to = user_address
        message.body = txt_body
        message.html = html_body
        message.send()
    else:
        pass

def send_test(sender_address, user_address, subject, body_template, body_values):
    # Html email template
    mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.html')
    html_body = template.render(mail_template, body_values, debug=_DEBUG)
    # Text email template
    mail_template = os.path.join(os.path.dirname(__file__), 'templates', body_template + '.txt')
    txt_body = template.render(mail_template, body_values, debug=_DEBUG)
    print("--- text ---")
    print(txt_body)
    print("\n--- html ---")
    print(html_body)


def test():
    body_values = {'firstname':'Fred', 'lastname':'Smith', 'address':'<script>alert("attack!")</script>',
                   'city':'<b>Bold?</b>', 'zipcode':'99999', 'country':'China', 'email':'hacker@china.gov', 'regkey':'2929'}
    user_email = 'john@rockfishnw.com'
    send_test(Company_email, Company_email, to_Company_subject, 'Company_email', body_values)
    send_test(Company_email, user_email, to_user_subject, 'user_email', body_values)
