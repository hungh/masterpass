#!/usr/bin/env python3

from distutils.core import setup

setup(name='MasterPswrd',
      version='1.0',
      description='Python3 distribution script for Master password',
      author='Hung Huynh',
      author_email='h.huynh@tmcbonds.com',
      url='http://www.tmcbonds.com',
      platforms='Linux',
      install_requires=['pymongo', 'py-bcrypt', ' pycrypto'],
      packages=['master', 'master.handler', 'master.beans', 'master.handler', 'master.httpcontroller',
                'master.logger', 'master.meta', 'master.mimecontroller', 'master.persistence', 'master.sesscontroller'])
