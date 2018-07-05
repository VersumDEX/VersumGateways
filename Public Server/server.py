from flask import Flask, request
import json
import MySQLdb
import hashlib
from Savoir import Savoir
from conf import *

app = Flask(__name__)

################################Versum############################################################
@app.route('/register',methods=['POST'])#run versum node as entry point for new connections AND 
def register_vaddress():		#to give send/receive rights to new users - this node has to be an admin node
    versum = Savoir(muser, \
                    mpassword , \
                    "127.0.0.1", mport, \
                    mchainname)
    raw_data = request.data
    data = json.loads(raw_data)
    try:
        versum.grant(data["vaddress"], "send")
        versum.grant(data["vaddress"], "receive")
        return "Success"
    except:
        return "Error"

##################################################################################################

################################Bitcoin###########################################################
##withdraw
@app.route('/btc/set/vaddress',methods=['POST'])#only accesible from worker server
def btc_set_unused_vaddress():                  #set pw --> use hashlib
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc": #add better security!!!
        sql = """INSERT INTO `unused_vaddresses`
            (`vaddress`)
            VALUES
            ('{}');""".format(data["vaddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
@app.route('/btc/len/vaddress',methods=['POST'])
def btc_len_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/get/vaddress',methods=['POST'])
def btc_get_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["raddress"]:
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        address_list = cur.fetchall()
        raddress = data["raddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `withdraw` (`raddress`, `vaddress`)\
                            VALUES ('{}', '{}');".format(\
                            raddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_vaddresses` WHERE \
                        `vaddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error No addresses"
    else:
        db.commit()
        cur.close()
        return "Error No data"

@app.route('/btc/get/withdrawdata',methods=['POST'])
def btc_get_withdraw_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `withdraw`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/del/withdrawdata',methods=['POST'])
def btc_del_withdraw_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    vaddress = data["vaddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `withdraw` WHERE\
                `vaddress`='{}';".format(vaddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"


##deposit
@app.route('/btc/set/raddress',methods=['POST'])
def btc_set_unused_raddress():  
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        sql = """INSERT INTO `unused_raddresses`
            (`raddress`)
            VALUES
            ('{}');""".format(data["raddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/len/raddress',methods=['POST'])
def btc_len_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_raddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/get/raddress',methods=['POST'])
def btc_get_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["vaddress"]:
        cur.execute("SELECT * FROM `unused_raddresses`;")
        address_list = cur.fetchall()
        vaddress = data["vaddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `deposit` (`vaddress`, `raddress`)\
                            VALUES ('{}', '{}');".format(\
                                vaddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_raddresses` WHERE \
                            `raddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/get/depositdata',methods=['POST'])
def btc_get_deposit_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `deposit`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/btc/del/depositdata',methods=['POST'])
def btc_del_deposit_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Bitcoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    raddress = data["raddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `deposit` WHERE `raddress`='{}';".format(raddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
##################################################################################################

################################Litecoin##########################################################
##withdraw
@app.route('/ltc/set/vaddress',methods=['POST'])#only accesible from worker server
def ltc_set_unused_vaddress():                  #set pw --> use hashlib
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        sql = """INSERT INTO `unused_vaddresses`
            (`vaddress`)
            VALUES
            ('{}');""".format(data["vaddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
@app.route('/ltc/len/vaddress',methods=['POST'])
def ltc_len_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/get/vaddress',methods=['POST'])
def ltc_get_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["raddress"]:
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        address_list = cur.fetchall()
        raddress = data["raddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `withdraw` (`raddress`, `vaddress`)\
                            VALUES ('{}', '{}');".format(\
                            raddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_vaddresses` WHERE \
                        `vaddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error No addresses"
    else:
        db.commit()
        cur.close()
        return "Error No data"

@app.route('/ltc/get/withdrawdata',methods=['POST'])
def ltc_get_withdraw_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `withdraw`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/del/withdrawdata',methods=['POST'])
def ltc_del_withdraw_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    vaddress = data["vaddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `withdraw` WHERE\
                `vaddress`='{}';".format(vaddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"


##deposit
@app.route('/ltc/set/raddress',methods=['POST'])
def ltc_set_unused_raddress():  
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        sql = """INSERT INTO `unused_raddresses`
            (`raddress`)
            VALUES
            ('{}');""".format(data["raddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/len/raddress',methods=['POST'])
def ltc_len_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_raddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/get/raddress',methods=['POST'])
def ltc_get_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["vaddress"]:
        cur.execute("SELECT * FROM `unused_raddresses`;")
        address_list = cur.fetchall()
        vaddress = data["vaddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `deposit` (`vaddress`, `raddress`)\
                            VALUES ('{}', '{}');".format(\
                                vaddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_raddresses` WHERE \
                            `raddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/get/depositdata',methods=['POST'])
def ltc_get_deposit_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `deposit`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/ltc/del/depositdata',methods=['POST'])
def ltc_del_deposit_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Litecoin")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    raddress = data["raddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `deposit` WHERE `raddress`='{}';".format(raddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
##################################################################################################

################################Ethereum##########################################################
##withdraw
@app.route('/eth/set/vaddress',methods=['POST'])#only accesible from worker server
def eth_set_unused_vaddress():                  #set pw --> use hashlib
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        sql = """INSERT INTO `unused_vaddresses`
            (`vaddress`)
            VALUES
            ('{}');""".format(data["vaddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
@app.route('/eth/len/vaddress',methods=['POST'])
def eth_len_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/get/vaddress',methods=['POST'])
def eth_get_unused_vaddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["raddress"]:
        cur.execute("SELECT * FROM `unused_vaddresses`;")
        address_list = cur.fetchall()
        raddress = data["raddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `withdraw` (`raddress`, `vaddress`)\
                            VALUES ('{}', '{}');".format(\
                            raddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_vaddresses` WHERE \
                        `vaddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error No addresses"
    else:
        db.commit()
        cur.close()
        return "Error No data"

@app.route('/eth/get/withdrawdata',methods=['POST'])
def eth_get_withdraw_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `withdraw`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/del/withdrawdata',methods=['POST'])
def eth_del_withdraw_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    vaddress = data["vaddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `withdraw` WHERE\
                `vaddress`='{}';".format(vaddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"


##deposit
@app.route('/eth/set/raddress',methods=['POST'])
def eth_set_unused_raddress():  
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()           
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        sql = """INSERT INTO `unused_raddresses`
            (`raddress`)
            VALUES
            ('{}');""".format(data["raddress"])
        cur.execute(sql)
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/len/raddress',methods=['POST'])
def eth_len_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("SELECT * FROM `unused_raddresses`;")
        data = cur.fetchall()
        db.commit()
        cur.close()
        return str(len(data))
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/get/raddress',methods=['POST'])
def eth_get_unused_raddress():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    if data["vaddress"]:
        cur.execute("SELECT * FROM `unused_raddresses`;")
        address_list = cur.fetchall()
        vaddress = data["vaddress"]
        if len(address_list) > 0:
            cur.execute("INSERT INTO `deposit` (`vaddress`, `raddress`)\
                            VALUES ('{}', '{}');".format(\
                                vaddress,address_list[0][0]))
            cur.execute("DELETE FROM `unused_raddresses` WHERE \
                            `raddress`='{}';".format(address_list[0][0]))
            db.commit()
            cur.close()
            return address_list[0]
        else:
            db.commit()
            cur.close()
            return "Error"
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/get/depositdata',methods=['POST'])
def eth_get_deposit_set():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("Select * FROM `deposit`;")
        raw_data = cur.fetchall()
        data = json.dumps({"data":raw_data})
        db.commit()
        cur.close()
        return data
    else:
        db.commit()
        cur.close()
        return "Error"

@app.route('/eth/del/depositdata',methods=['POST'])
def eth_del_deposit_data():
    db = MySQLdb.connect(host="localhost", user=myuser, passwd=mypassword, \
                         db="Ethereum")
    cur = db.cursor()
    raw_data = request.data
    data = json.loads(raw_data)
    raddress = data["raddress"]
    m = hashlib.sha256()
    m.update(data["password"])
    if m.digest() == "\xaa\x05uO<\x03B\x8ca\xa7\xf9fb\xf9\x02\xa0(I\xc1s\x98\xe9\xfb\xeer$c\xda\x1b\xa2\xff\xcc":
        cur.execute("DELETE FROM `deposit` WHERE `raddress`='{}';".format(raddress))
        db.commit()
        cur.close()
        return "Success"
    else:
        db.commit()
        cur.close()
        return "Error"
    
