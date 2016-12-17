import smtplib

message = """To: john@Company.com
From: info@rockfishnw.com
Subject: Registration Key
Content-type: text/html

<html>
	<head>
		<meta http-equiv="content-type" content="text/html;charset=UTF-8" />
	</head>
	<body style="font-family:Trebuchet MS, arial, helvetica, sans-serif;">
		<div style="margin-bottom:40px;">
			<img src="http://www.Company.com/images/logo.jpg" />
		</div>
		<div style="margin:40px">
			<h1 style="font-size:16px;">Thank you for registering.</h1>
			<p>Please go to <a href="http://updates.Company.com/login">http://updates.Company.com/login</a>
				to login with your email address and registration key. You can then
				download the latest software versions.
			</p>
			<p>Your registration key:  <b>2492F669E81CA6F765494EC00DD8BA5E</b></p>
			<p>Thank you,<br />
				Company Technologies
			</p>
		</div>
	</body>
</html>
"""

Company_email = "info@Company.com"
Company_pwd = "smtp_password!!"

user_address = "john@Company.com"
john_email = "John <john@Company.com>"

rockfish_info = "info@rockfishnw.com"
rockfish_info_pwd = "smtp_password!!"

from_address = Company_email

sender_address = 'Company' # @Company.webfactional.com'
sender_pwd = "smtp_password!!"

to_user_subject = "Company registration confirmation"
to_Company_subject = "New user registration information"


s = smtplib.SMTP()
s.connect('smtp.webfaction.com')
s.login(sender_address, sender_pwd)
s.sendmail(from_address, user_address, message)

