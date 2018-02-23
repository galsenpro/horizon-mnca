from urllib2 import Request, urlopen

values = """
  {
    "entity_type": "entity_typeUpdate"
  }
"""

headers = {
  'Content-Type': 'application/json',
  'Fiware-Service': 'portal',
  'Fiware-ServicePath': '/subservportal'
}
request = Request('http://iot.testnca.org:4041/iot/services?resource=/iot/d&apikey=API8', data=values, headers=headers)
request.get_method = lambda: 'PUT'

response_body = urlopen(request).read()
print response_body
