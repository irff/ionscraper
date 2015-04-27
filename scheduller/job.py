import sys
import requests
import logging
from time import sleep

logging.basicConfig(filename='job.log',level=logging.INFO)

URL = "http://128.199.116.101:9009"
USER = "ionscraper"
PASS = "m4nt4bg4n"
STOP_ALL = URL + "/index.html?action=stopall"

if len(sys.argv) < 3:
    exit()

if sys.argv[1] not in ["start","stop","restart"]:
    exit()

action = sys.argv[1]

requests.get(STOP_ALL, auth=(USER, PASS))
sleep(10)
proccessname = sys.argv[2]
command = URL + "/index.html?processname=" + proccessname + "&action=" + action

requests.get(command, auth=(USER, PASS))

logging.info("starting " + proccessname + " command: " + command)
exit()