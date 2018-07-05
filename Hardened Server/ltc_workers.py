from jsonrpc_requests import Server
from Savoir import Savoir
from requests import post
from threading import Thread
import time
import json
from conf import *

if __name__ == "__main__":
    ltc = Server("http://127.0.0.1:"+bport, auth=(buser,\
                                                bpassword))
    versum = Savoir(muser, \
                    mpassword, \
                    "localhost", mport, \
                    mchainname)
    url = publicserver+"/ltc/"

def refill_raddresses():
    """
    Ensures that always deposit addresses are available in the Database
    """
    while True:
        try:
            data = json.dumps({"password":publicserverpassword})
            r = post(url + "len/raddress", data).text
            if int(r) < 100:
                raddress = ltc.getnewaddress()
                data = json.dumps({"password":publicserverpassword,\
                               "raddress": raddress})
                r = post(url + "set/raddress", data).text
        except:
            pass
        time.sleep(60)

def deposit_worker():
    """
    Check every address in database for deposits and executes them
    """
    while True:
        try:
            data = json.dumps({"password":publicserverpassword})
            r = post(url + "get/depositdata", data).json()
            address_data = r["data"]
            for pair in address_data:
                raddress = pair[0]
                vaddress = pair[1]
                value = ltc.getreceivedbyaddress(raddress)
                if value > 0:
                    data = json.dumps({"raddress": raddress,\
                                       "password":publicserverpassword})
                    r = post(url + "del/depositdata", data).text
                    if r == "Success":
                        print versum.issuemore(vaddress, "LTC", value)
        except:
            pass
        time.sleep(60)

def refill_vaddresses():
    """
    Ensures that always enough withdraw addresses are available
    """
    while True:
        try:
            data = json.dumps({"password":publicserverpassword})
            r = post(url + "len/vaddress", data).text
            if int(r) < 100:
                vaddress = versum.getnewaddress()
                versum.grant(vaddress, "send")
                versum.grant(vaddress, "receive")
                data = json.dumps({"password":publicserverpassword,\
                                   "vaddress": vaddress})
                r = post(url + "set/vaddress", data).text
        except:
            pass
        time.sleep(60)
        

def withdraw_worker():
    """
    Checks every address in database for withdrawals and executes them.
    Afterward burns assets
    """
    while True:
        try:
            data = json.dumps({"password":publicserverpassword})
            r = post(url + "get/withdrawdata", data).json()
            address_data = r["data"]
            for pair in address_data:
                raddress = pair[1]
                vaddress = pair[0]
                value_list = versum.getaddressbalances(vaddress)
                for asst in value_list:
                    if asst["name"] == "LTC":
                        value = float(asst["qty"])
                        if value > 0:
                            data = json.dumps({"vaddress": vaddress,\
                                       "password":publicserverpassword})
                            r = post(url + "del/withdrawdata", data).text
                            if r == "Success":
                                print ltc.sendtoaddress(raddress, (value*0.995)-0.001)
                                versum.sendassetfrom(vaddress, \
                                    "1XXXXXXXKhXXXXXXTzXXXXXXY6XXXXXXX5UtyF",\
                                    "LTC", value) 
        except:
            pass
        time.sleep(60)

def run_all():
    Thread(target=refill_raddresses).start()
    Thread(target=deposit_worker).start()
    Thread(target=refill_vaddresses).start()
    Thread(target=withdraw_worker).start()
run_all()
