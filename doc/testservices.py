"""
@Auteur : Adama
"""
import requests
import json
import random
random = random.SystemRandom()
IDAS_URL = "http://172.16.207.118:4041/iot"
FIWARESERVICE = 'mncaservice'
FIWARESERVICEPATH = '/mncasubservice'
ALLSERVICESPATH = '/*'
CBROKER = "http://172.16.207.118:1026"
RESOURCE = "/iot/d"

"""
    --------- SERVICES ------------
    /services                :  all services
    /newservice              :  add a new service
    /ups/{apikey}/{resource} :  update a service
    /dels/{apikey}/{resource}:  delete a service

    --------- DEVICES ------------
    /devices                 :  all devices
    /newdevice               :  add a new device
    /upd/{device_id}         :  update a device
    /deld/{device_id}        :  delete a device
"""

""" Generate un APIKEY """
def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """ Returns a securely generated random string.
        The default length of 12 with the a-z, A-Z, 0-9 character set returns
        a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.
        Taken from the django.utils.crypto module.
    """
    return ''.join(random.choice(allowed_chars) for i in range(length))
 
def get_secret_key(branch = ""):
    """ Create a random secret key.
        Taken from the Django project.
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABSCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return branch + get_random_string(6, chars)

""" Retrieve all services of IDAS """
def get_services(service = FIWARESERVICE, subservice = ALLSERVICESPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': subservice
        }
        idasResponse = requests.get(IDAS_URL+"/services", headers = headers)
        return idasResponse.json()
    except Exception as x:
        return x


""" Details of a specific service """
def describe_service(service_id, service = FIWARESERVICE, subservice = ALLSERVICESPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': subservice
        }
        idasResponse =  requests.get(IDAS_URL+"/services" + '/{:d}/'.format(service_id), headers = headers)
        return idasResponse
    except Exception  as x:
        return x

""" Add a new service on IDAS """
def add_service(service =  FIWARESERVICE, subservice = FIWARESERVICEPATH,
                cbroker = CBROKER, 
                resource = RESOURCE , 
                entity_type = "obj-test"):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': str(subservice)
        }
        key = get_secret_key()
        dbody ={
            "services": [{
                    "apikey": str(key),
                    "cbroker": str(cbroker),
                    "resource": str(resource),
                    "entity_type": str(entity_type), 
                    "attributes": [{
                        "name": "status",
                        "type": "string",
                        "object_id": "s"
                        },{
                            "name": "temperature",
                            "type": "float",
                            "object_id": "t"
                        },{
                            "name": "humidity",
                            "type": "float",
                            "object_id": "h"
                        }
                    ],
                    "static_attributes": [{
                          "name": "mystatic1",
                          "type": "string",
                          "value": "machin"
                        },{
                          "name": "mystatic2",
                          "type": "string",
                          "value": "bidule"
                        }
                    ],
                    "internal_attributes": [{
                          "name": "myinternal1",
                          "type": "string",
                          "value": "machin"
                        },{
                          "name": "myinternal2",
                          "type": "float",
                          "value": "67.99"
                        }
                    ]
                }]
            }
        idasResponse = requests.post(IDAS_URL+"/services", data= json.dumps(dbody), headers = headers)
        #print(json.dumps(dbody))
        return idasResponse
    except Exception as x:
        return x

""" Update a specific service """
def update_service(apikey, 
                    resource = RESOURCE, 
                    device = None):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': FIWARESERVICE,
            'Fiware-ServicePath': FIWARESERVICEPATH
        }
        dbody = """
          {
            "entity_type": "Update"
          }
        """
        params = { 'resource': str(resource),
                   'apikey': str(apikey)
        }
        print(url)
        print(headers)
        print(dbody)
        idasResponse =  requests.put(IDAS_URL+"/services", params = params, data= dbody, headers = headers)
        return idasResponse
    except Exception as x:
        return x

""" Delete a specific service on IDAS """
def delete_service(service_apikey, resource = "/iot/d", service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': str(subservice)
        }
        params = { 'apikey': str(service_apikey),
                   'resource': str(resource)
        }
        idasResponse = requests.delete(IDAS_URL+"/services", params = params, headers = headers)
        return idasResponse
    except Exception as x:
        return x

""" Add a new device on IDAS """
def add_device(deviceName = "Device", entityName = "Machine", protocole = "JSON", service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': str(service),
            'Fiware-ServicePath': str(subservice)
        }
        key = get_secret_key()
        dbody ={
            "devices": [{
                "device_id": str(deviceName) + str(countDevices(str(service), str(subservice)) +1),
                "entity_name": str(entityName),
                "protocol": str(protocole),
                "entity_type": "thing",
                "timezone": "Europe/Madrid",
                "attributes": [{
                    "object_id": "t",
                    "name": "temperature",
                    "type": "int"
                }],
                "commands": [{
                    "name": "ping",
                    "type": "command",
                    "value": "Machine-sensor@ping"
                }],
                "static_attributes": [{
                    "name": "color",
                    "type": "string",
                    "value": "value"
                }]
            }]
        }
        print(IDAS_URL+"/devices?protocol="+protocole)
        print(headers)
        print(dbody)
        params = { 'protocol': str(protocole)}
        idasResponse = requests.post(IDAS_URL+"/devices", params = params, data= json.dumps(dbody), headers = headers)
        #print(json.dumps(dbody))
        return idasResponse
    except Exception as x:
        return x

""" Retrieve all devices """
def get_devices(service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': subservice
        }
        idasResponse = requests.get(IDAS_URL+"/devices", headers = headers)
        return idasResponse.json()['count']
    except Exception as x:
        return x

def countDevices(service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': subservice
        }
        idasResponse = requests.get(IDAS_URL+"/devices", headers = headers)
        return idasResponse.json()['count']
    except Exception as x:
        return -1

""" Delete a specific device on IDAS """
def delete_device(device_id, service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': str(subservice)
        }
        idasResponse = requests.delete(IDAS_URL+"/devices/"+ str(device_id), headers = headers)
        return idasResponse
    except Exception as x:
        return x

""" Update a specific device on IDAS """
def update_device(device_id, service = FIWARESERVICE, subservice = FIWARESERVICEPATH):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': service,
            'Fiware-ServicePath': str(subservice)
        }
        dbody = {
          "static_attributes": [
                {
                  "name": "location",
                  "type": "string",
                  "value": "43.66756, 7.21334"
                },{
                  "name": "max-power",
                  "type": "integer",
                  "value": "300"
                }
            ]
        }
        idasResponse = requests.put(IDAS_URL+"/devices/"+ str(device_id), data = json.dumps(dbody), headers = headers)
        return idasResponse
    except Exception as x:
        return x
newdevice = add_device()
print(newdevice)
devices = get_devices()
print(devices)
deldevice = delete_device("Device1")
"""Update service """
#maj = update_service("API8")
#print(maj)