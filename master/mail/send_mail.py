from master.consts import MAIL_USER_NAME, GMAIL_SMTP, TSL_PORT
from master.logger.file_logger import logger
import smtplib


def send_gmail(receiver, message, smtp_password):
    """

    :param receiver: string email of receiver
    :param message:  string mail content
    :return: None
    """
    server = smtplib.SMTP(GMAIL_SMTP, TSL_PORT)
    server.ehlo()
    server.starttls()
    msg = "Subject: Secure Storage - Reset Password\r\n\r\n " + message


    mail_user_name = MAIL_USER_NAME
    server.login(mail_user_name,smtp_password)
    server.sendmail(MAIL_USER_NAME, receiver, msg)
    logger().info('sent email to {}'.format(receiver))

