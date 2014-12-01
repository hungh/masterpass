# Quick test to make sure all dependencies are satisfied
version=`python3 --version | cut -d" " -f2 |grep 3.4`
if [ -z ${version} ] ; then
   echo "Python version 3.4.x is required"
   exit 1;
fi
C1=`python3 -c 'import pymongo' 2>&1 | grep Error`
C2=`python3 -c 'import bcrypt' 2>&1 | grep Error`

if [ -z "$C1$C2" ]; then
  echo "All dependencies have been satisfied. "
else
  echo $C1
  echo $C2
fi
