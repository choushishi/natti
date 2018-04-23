import urllib.request
import getpass
from twilio.rest import Client
import time

account_sid = getpass.getpass("sid: ")
auth_token = getpass.getpass("token: ")
from_nmb = getpass.getpass("from: ")
to_nmb = getpass.getpass("to: ")

client = Client(account_sid, auth_token)

url = "https://www.naati.com.au/other-information/ccl-testing/"
cached = urllib.request.urlopen(url).read()

starttime = time.time()
refresh = 60.0
while True:
    print("tick")
    latest = urllib.request.urlopen(url).read()
    diff = b""
    if latest != cached:
        print("diff!")
        diff += b"diff detected:\n"
        count = 0
        for pair in zip(latest.splitlines(), cached.splitlines()):
            if pair[0] != pair[1]:
                diff += pair[0] + b" " + pair[1] + b"\n"
                print(pair[0], pair[1])
                if count > 5:
                    break
                count += 1

        print("sending message")
        message = client.messages.create(to=to_nmb, from_=from_nmb, body=diff.decode("utf-8"))
        cached = latest
    time.sleep(refresh - ((time.time() - starttime) % refresh))
