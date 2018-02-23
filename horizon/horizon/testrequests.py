import requests, json
def requete():
    url = "http://iot.testnca.org:4041/iot/services?apikey=API8&resource=/iot/d"
    headers = {
                    "content-type": "application/json",
                    "Fiware-Service": "portal",
                    "Fiware-ServicePath": "/subservportal"
        }
    values ={
                'entity_type': 'entity_updatefiware'
        }
    #print(json.dumps(values))
    #response = requests.put(url=url,  data=json.dumps(values), headers=headers)
    response = requests.put(url=url,  data="""{'entity_type': 'entity_updatefiware'}""", headers=headers)
    print(response.status_code)
    print(response.headers)

requete()