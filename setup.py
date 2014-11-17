#!/usr/bin/env python3

from distutils.core import setup

setup(name='masterpass',
      version='1.0',
      description='Python3 distribution script for Master Password',
      author='Hung Huynh',
      author_email='hungcs@gmail.com',
      url='http://www.apache.org',
      platforms='Linux',
      install_requires=['pymongo', 'py-bcrypt', ' pycrypto'],
      packages=['master', 'master.handler', 'master.beans', 'master.handler', 'master.httpcontroller',
                'master.logger', 'master.meta', 'master.mimecontroller', 'master.persistence', 'master.sesscontroller'])