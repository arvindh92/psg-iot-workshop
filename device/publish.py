'''
Created on 25-Feb-2018

@author: Arvind
'''
from paho.mqtt import client as mqtt

import time
from urllib.parse import quote_plus, urlencode
from base64 import b64encode, b64decode
from hmac import HMAC
from _sha256 import sha256
from pip._vendor.distlib.compat import raw_input
import threading
import ssl


device_id = "galelio"
SASKey = "+iOBgWWOjzkbbGjHAarWsqozclf5gmxAd27/wi09pCw="

iot_hub_name = "psg"
path_to_root_cert = "./rootca.pem"


def get_sas():

    uri ="{}/devices/{}".format(iot_hub_name+".azure-devices.net",device_id)
    key = SASKey
    policy_name = None
    expiry = 30
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
    signature = b64encode(HMAC(b64decode(key), sign_key.encode(encoding='utf_8'), sha256).digest())
    rawtoken = {
        'sr' :  uri,
        'sig': signature,
        'se' : str(int(ttl))
        }
    if policy_name is not None:
        rawtoken['skn'] = policy_name
    return 'SharedAccessSignature ' + urlencode(rawtoken)
sas_token = get_sas()


pub_topic = "devices/" + device_id + "/messages/events/"
sub_topic = "devices/"+device_id+"/messages/devicebound/#"


def on_connect(client, userdata, flags, rc):
    print ("Device connected with result code: " + str(rc))
    client.subscribe(sub_topic) 

def on_message(client, userdata, msg):
    print(msg.payload)

def on_disconnect(client, userdata, rc):
    print ("Device disconnected with result code: ", userdata, str(rc))

def on_publish(client, userdata, mid):
    print ("Device sent message")

client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.tls_insecure_set(False)

client.username_pw_set(username=iot_hub_name+".azure-devices.net/" + device_id+"/api-version=2016-11-14", password=sas_token)


client.connect(iot_hub_name+".azure-devices.net", port=8883)


def publish_data():
    global client
    global on_message
    global sub_topic
    data = "0,0,0"
    while data is not "e":
        
        data = raw_input("status? ")
        type(data)
        if(data is not "e"):
            client.publish(pub_topic,data, qos =1)
    #client.disconnect()
       
t1 = threading.Thread(target=publish_data)
t1.start()
t1.join()


client.loop_forever()


