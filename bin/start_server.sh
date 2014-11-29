#!/bin/bash
echo "Please make sure you start MongoDB.";
echo "And have mongod listening port configured in master.consts.py";

if [ "$#" -ne 2 ] ; then
   echo "please pass a port number and SMTP server password";
else   
   PROJECT_HOME=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )
   PYTHONPATH=${PROJECT_HOME}
   export PYTHONPATH
   python3  ${PROJECT_HOME}/main.py $1 $2
fi
