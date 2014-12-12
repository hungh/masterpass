masterpass
==========

Master Password Web Server

This application is written in Python 3.4 with Mongo DB back-end database and AngularJS as front-end.
The web server is using Python HTTP request handler.

IMPORTANT:
---------

* Default admin access is root/password. 
* You must change root password after first login.
* All users passwords are hashed with bcrypt.
* Users' data is encrypted using BlowFish.  
 

REQUIREMENTS:
------------

* Python 3.4.x
* bcrypt 
* pycrypto
* pymongo 
* MongoDB 


INSTALLATION:
-------------

* On Ubuntu or other environments:

  $ sudo apt-get install python3.4-dev

* bcrypt:

  $ pip install bcrypt

  or,

  $ wget https://py-bcrypt.googlecode.com/files/py-bcrypt-0.4.tar.gz 

  $ cd py-bcrypt-0.4

  $ sudo python3 setup.py install

  You might need to run this command to install libffi if the above command fails
  
  $ sudo apt-get install  libffi-dev 


* pycrypto:

  $ pip install pycrypto


* pyMongo:

  $ pip install pymongo

  or, install from source

  $ git clone git://github.com/mongodb/mongo-python-driver.git pymongo

  $ cd pymongo/

  $ sudo python3 setup.py install


* MongoDB:

  Download link: 
  https://www.mongodb.org/downloads


* Change the following values in the consts.py if your database runs on a different port:

  DB_SERVER_PORT = 27017

* To start mongodb:

   mongod --dbpath=/dir/to/data

   This will start MongoDB server at default port 27017

   To use a different port, use --port number


START/STOP SERVER:
-----------------

* To start/stop server:

  ./bin/start_server.sh

  ./bin/stop_server.sh port_number

