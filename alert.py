# Python code to illustrate Sending mail from 
# your Gmail account 
import smtplib

def send_alert(msg):
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	  
	# start TLS for security
	s.starttls()
	  
	# Authentication
	s.login("sender@email.com", "sender_password")
	  
	# message to be sent
	message = "Alert!! Your missing vehicle has been found at: " + msg
	  
	# sending the mail
	s.sendmail("sender@email.com", "receiver@email.com", message)
	  
	# terminating the session
	s.quit()