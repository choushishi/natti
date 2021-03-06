import urllib.request
import getpass
from twilio.rest import Client
import time
import difflib
import datetime

# twilio configurations
print("Please enter your twilio project account details: ")
account_sid = getpass.getpass("sid: ")
auth_token = getpass.getpass("token: ")
from_nmb = getpass.getpass("from: ")
to_nmb = getpass.getpass("to: ")
client = Client(account_sid, auth_token)

# monitor setup
refresh = float(input("Entering refreshing rate in seconds: "))
url = "https://www.naati.com.au/other-information/ccl-testing/"
cached = urllib.request.urlopen(url).read().decode("utf-8").splitlines()
cached = ["test"] + cached  # tesing twilio on first iteration
starttime = time.time()

# initialize differ
d = difflib.Differ()


def log(msg):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + msg)


# main loop
while True:
    log("tick")
    latest = urllib.request.urlopen(url).read().decode("utf-8").splitlines()
    diff = d.compare(cached, latest)
    if cached != latest:
        log("diff!")
        diff = "\n".join([l for l in diff if l.startswith('+ ') or l.startswith('- ')])  # only send differences
        diff = diff[:130]  # limit sms body to 130 characters
        log(diff)
        log("sending message")
        message = client.messages.create(to=to_nmb, from_=from_nmb, body=diff)
        log("message sent")
        cached = latest
    time.sleep(refresh - ((time.time() - starttime) % refresh))
