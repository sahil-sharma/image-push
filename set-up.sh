#!/bin/bash -ex

if [ `whoami` != 'root' ]
  then
    echo "You must be root to do this."
    exit
fi

#Setting up system
apt update && apt install awscli -y
wget https://bootstrap.pypa.io/get-pip.py
chmod a+x get-pip.py
python get-pip.py
pip install virtualenv
virtual /opt/task
source /opt/task/bin/activate
pip install -r ./requirements.txt
python main.py &
echo -e ""
echo -e "Your application is up and running. You can access it as mentioned below"

$ curl http://localhots:5000/
echo -e ""

echo -e "Verify download and push to s3 API end-point (/download)"
$ curl http://localhost:5000/download\?url\=https://www.hdwallpapers.in/download/battlefield_4_soldier_5k-1280x720.jpg
$ curl http://localhost:5000/download\?url\=https://www.hdwallpapers.in/download/maleficent_mistress_of_evil_angelina_jolie_2019_4k-480x800.jpg
$ curl http://localhost:5000/download\?https://apod.nasa.gov/apod/image/1701/potw1636aN159_HST_2048.jpg

echo -e "Verify list contents API end-point (/list)"
$ curl http://localhost:5000/list

echo -e ""
