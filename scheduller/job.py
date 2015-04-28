import sys
import requests
import logging
from datetime import datetime
from time import sleep

logging.basicConfig(filename='job.log',level=logging.INFO)

URL = "http://128.199.116.101:9009"
USER = "ionscraper"
PASS = "m4nt4bg4n"
STOP_ALL = URL + "/index.html?action=stopall"

if len(sys.argv) < 3:
    logging.info(date_log + "Error command")
    exit()

if sys.argv[1] not in ["start","stop","restart"]:
    logging.info(date_log + "Error command")
    exit()

action = sys.argv[1]

requests.get(STOP_ALL, auth=(USER, PASS))
sleep(30)
proccessname = sys.argv[2]
command = URL + "/index.html?processname=" + proccessname + "&action=" + action

requests.get(command, auth=(USER, PASS))
date_log = "[" + str(datetime.now()) + "]"
logging.info(date_log + "starting " + proccessname + " command: " + command)
exit()