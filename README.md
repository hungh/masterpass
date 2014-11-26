masterpass
==========

Master Password Web Server

This application is written in Python 3.4 with Mongo DB back-end database and AngularJS as front-end.
The web server is using Python HTTP request handler.

IMPORTANT:
---------

* You must change root password (TODO:) before setting up and using this application.
* All users passwords are hashed with bcrypt.
* Each data entry (which is a user name and password pair) belonging to a login user is encrypted
  with password entry as key using BlowFish
* Default root password to enter the application is 'password', once you log in as root you must change
  your password.
 

REQUIREMENTS:
------------

* Python dev 3.4, to install on Debian environment:

  $ sudo apt-get install python3.4-dev

* bcrypt:

  $ pip install bcrypt

  or,
  $ wget https://code.google.com/p/py-bcrypt/downloads/detail?name=py-bcrypt-0.4.tar.gz&can=2&q=
  $ cd py-bcrypt-0.4
  sudo python3 setup.py install

  Note: on Ubuntu or Mint, you might need to run this command to install libffi
  
  sudo apt-get install  libffi-dev 


* PyMongo:

  pip install pymongo

  or, install from source

  $ git clone git://github.com/mongodb/mongo-python-driver.git pymongo
  $ cd pymongo/
  $ python setup.py install

  Installation for Python 3
  $ git clone git://github.com/mongodb/mongo-python-driver.git pymongo
  $ cd pymongo/
  $ sudo python3 setup.py install

* MongoDB:

  Download link: 
  https://www.mongodb.org/downloads



INSTALLATION:
-------------

* under 'masterpass', change the following values in the consts.py file for your need:

  USER_HOME = '/home/dir/'

  PROJECT_HOME = '/home/dir/masterpass'  

  DB_USERS_LOCATION = '/home/dir/data/db/users.db'  

  DB_SERVER_PORT = 27017

* To start mongodb:

   mongod --dbpath

   This will start MongoDB server at default port 27017

   To use a different port, use --port number


START/STOP SERVER:
-----------------

* To start server:

  From project home masterpass, type

  ./bin/start_server.sh port_number

  ./bin/stop_server.sh port_number 

  to stop


