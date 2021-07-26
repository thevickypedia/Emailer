sudo apt-get update
sleep 2
sudo apt-get install python3 python3-pip
sleep 2
python3 -m venv venv
sleep 2
source venv/bin/activate
sleep 2
pip3 install -r requirements.txt
