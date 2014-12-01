from master.consts import TSL_PORT, GMAIL_SMTP
from master.logger.file_logger import logger
from master.beans.nosession import AuthHolder
from email.mime.text import MIMEText
import smtplib

MAIL_SUBJECT = 'Secure Storage - Reset Password'


def send_gmail(receiver, message, smtp_password):
    """

    :param receiver: string email of receiver
    :param message:  string mail content
    :return: None
    """
    server = smtplib.SMTP(AuthHolder().get_smtp_server(), TSL_PORT)
    server.ehlo()
    server.starttls()
    msg = "Subject: {}\r\n\r\n {}".format(MAIL_SUBJECT, message)
    mail_user_name = AuthHolder().get_google_mail()
    server.login(mail_user_name, smtp_password)
    server.sendmail(mail_user_name, receiver, msg)
    logger().info('sent email to {}'.format(receiver))


def send_my_mail(receiver, message, smtp_server):
    msg = MIMEText(message)
    msg['Subject'] = MAIL_SUBJECT
    msg['From'] = AuthHolder().get_google_mail()
    msg['To'] = receiver
    s = smtplib.SMTP(smtp_server)
    s.send_message(msg)
    s.quit()


def send_mail(receiver, message):
    smtp_server = AuthHolder().get_smtp_server()
    if smtp_server == GMAIL_SMTP:
        send_gmail(receiver, message, AuthHolder().get_google_mail_pass())
    else:
        send_my_mail(receiver, message, smtp_server)



