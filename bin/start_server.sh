#!/bin/bash

if [ ! -z $1 ] ;then
    echo "This is an interactive script and therefore does not take any command line arguments."
    exit 1;
fi
options=""    
read -p "Please enter HTTP server port number('8009'):" WEB_PORT
if [ ! -z ${WEB_PORT} ] ; then
	options=${options}"--webport "${WEB_PORT}" "
fi
echo;
HOST_NAME=`hostname`
read -p "Please enter HTTP server host name(${HOST_NAME}):" WEB_SERVER_HOST
if [ -z ${WEB_SERVER_HOST} ] ; then
	options=${options}"--webhost "${HOST_NAME}" "
fi
echo;

read -p "Would you like using Google SMTP (y/N)" USE_SMTP 

if [ "${USE_SMTP}" == "y" ]; then	
		read -p "Please enter gmail address('publicsmtp1@gmail.com'):" GMAIL_ADDRESS
		if [ ! -z ${GMAIL_ADDRESS} ]; then
			options=${options}"--gmail "${GMAIL_ADDRESS}" "
		fi
		echo;
		while [ -z ${SMTP_PASSWORD} ]; do
			read -s -p "Please enter SMTP password:" SMTP_PASSWORD
			echo;
		done
		options=${options}"--gmailpass "${SMTP_PASSWORD}" "

		echo "Make sure you enable 'Access for less secure apps' in Account/Security"
else
		read -p "Please enter your SMTP server name('localhost'):" SMTP_SERVER
		if [ ! -z ${SMTP_SERVER} ] ; then
			options=${options}"--smtpserver "${SMTP_SERVER}" "
		fi
fi

read -p "Please enter mongod host name or ip address('localhost'):" MONGOD_SERVER 
if [ ! -z ${MONGOD_SERVER} ]; then
	options=${options}"--mongodserver "${MONGOD_SERVER}" "
fi
echo;

PROJECT_HOME=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )
PYTHONPATH=${PROJECT_HOME}
export PYTHONPATH
python3  ${PROJECT_HOME}/main.py ${options} $1

