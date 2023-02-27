# import smtplib
#
# smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
# smtp_obj.starttls()
# smtp_obj.login("kurban.63.axmedov@gmail.com", "kuba63kastro")
# smtp_obj.sendmail("kurban.63.axmedov@gmail.com", "stanleykurbick63@gmail.com", "поздравляю!")
# help(smtp_obj)
# smtp_obj.quit()

import smtplib, ssl
# #
# smtp_server = "smtp.mail.ru"
# port = 465  # For starttls
# sender_email = "kurban.63.axmedov@gmail.com"
# password = "lkhhdcocbzrvhlhd"
# MAIL_USERNAME="terra_test@internet.ru"
# MAIL_PASSWORD="pMCEpeMSqrgYEPD9pj4s"
# # Create a secure SSL context
# context = ssl.create_default_context()
#
# # Try to log in to server and send email
# # try:
# server = smtplib.SMTP(smtp_server,port)
# # server.ehlo() # Can be omitted
# server.starttls(context=context) # Secure the connection
# # server.ehlo() # Can be omitted
# server.login(MAIL_USERNAME, MAIL_PASSWORD)
# server.sendmail(MAIL_USERNAME, "malkolm.63.zed@mail.ru", "success!")

# TODO: Send email here
# except Exception as e:
#     # Print any error messages to stdout
#     print(e)
# finally:
#     server.quit()

import smtplib, ssl

port = 587  # For SSL
smtp_server = "smtp.mail.ru"
# MAIL_USERNAME = "terra_test@internet.ru"
MAIL_USERNAME = "malkolm.63.zed@mail.ru"
MAIL_PASSWORD = "2FeynEHRRSHRMxnBFJuw"
# password = input("Type your password and press enter: ")
message = "success"

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    server.sendmail(MAIL_USERNAME, "frenkjust@mail.ru", message)
