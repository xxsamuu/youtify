!/bin/bash

#for installing each package from other venv to this one.
if ["$1"  == ""]
then
echo "need to pass argument. Example: ./install_from_other_venv.sh requirements.txt"

else
cat $1 | while read line;do pip install  $line;  done
fi
