#!/bin/sh


if [ "$#" -ne 1 ] ; then
   echo "please pass a port number";
else
   port_num=$1
   process_id=`netstat  -ap 2>&1  | grep ${port_num} |  egrep -o 'LISTEN\s*[0-9]*/python3' | egrep  -o '[0-9]*/' | cut -d/ -f1`
   if [ ! -z  "$process_id" ] ; then
   	echo "Shutting down ${process_id}"
	kill  -9 ${process_id}
	echo "Checking if port is shutdown completely..."
	while [ True ]; do
	    binding_port=`netstat  -ap 2>&1 | egrep -o ${port_num}`
	    if [ -z ${binding_port} ] ; then
	        break;
	    fi
	    sleep 2
	    echo ">>>>>>>"
	done;

   else
   	echo "No listening port with ${port_num} is running" 
  fi
fi
