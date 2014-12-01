from master.beans.nosession import AuthHolder
from master.handler.main_server import MainHttpServer
from master.boostrap import initialize
from master.consts import DEFAULT_PORT, MAIL_USER_NAME, GMAIL_SMTP, DB_SERVER_HOST, WEB_SERVER_HOST
import argparse


def main():
    """
    Beta version of a Simple HTTP server
       by 'Hung Huynh'
    """
    parser = argparse.ArgumentParser(description="Python Web Server Options")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-p", "--webport", type=int, default=DEFAULT_PORT, help="Web server binding port")
    parser.add_argument("-j", "--webhost", default=WEB_SERVER_HOST, help="Web server host name")
    parser.add_argument("-g", "--gmail", default=MAIL_USER_NAME, help="Gmail address")
    parser.add_argument("-a", "--gmailpass", help="Gmail password.", default="")
    parser.add_argument("-m", "--smtpserver", default=GMAIL_SMTP, help="SMTP server name")
    parser.add_argument("-d", "--mongodserver", default=DB_SERVER_HOST, help="MongoDB server name")

    args = parser.parse_args()

    # initialize auth holder
    h = AuthHolder(web_server_port=args.webport,
                   google_mail=args.gmail,
                   google_mail_pass=args.gmailpass,
                   smtp_server=args.smtpserver,
                   mongod_server=args.mongodserver,
                   web_host_name=args.webhost)
    if args.quiet:
        print('Listening on ' + args.webport)
    elif args.verbose:
        print(h)

    initialize()
    MainHttpServer.start(args.webport)
    print("Termination is in progress. Please wait...")


if __name__ == "__main__":
    main()







