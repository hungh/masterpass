if [ "$#" -ne 1 ] ; then
   echo "please pass a port number";
else
   port_num=$1
   bind_port=`netstat  -ap 2>&1  | grep $port_num |  egrep -o 'LISTEN\s*[0-9]*/python3' | egrep  -o '[0-9]*/' | cut -d/ -f1`
   if [ ! -z  "$bind_port" ] ; then
   	echo "Shutting down ${bind_port}"
	kill  -9 ${bind_port}
   else
   	echo "No listening port with ${port_num} is running" 
  fi
fi
