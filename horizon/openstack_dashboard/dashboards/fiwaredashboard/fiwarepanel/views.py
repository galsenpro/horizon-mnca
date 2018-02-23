# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

#from horizon import views
from horizon import tabs, views
from openstack_dashboard.dashboards.fiwaredashboard.fiwarepanel  import tabs as fiwaredashboard_tabs

from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import newServiceForm

"""
Modules:
    - requests : pour effectuer des requetes dans idas
    - render : pour les rendus
    - json : pour les retours d'APi en json object 
"""
import requests
from django.shortcuts import render
import json
from django.template.defaulttags import register

#class IndexView(views.APIView):
class IndexView(tabs.TabbedTableView):
    tab_group_class = fiwaredashboard_tabs.FiwarepanelTabs
    # A very simple class-based view...
    template_name = 'fiwarepanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context['panel_name'] = "fiwarepanel"
        return context

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class ServicesIdasView(views.APIView):
    tab_group_class = fiwaredashboard_tabs.FiwarepanelTabs
    template_name = 'fiwarepanel/retrieveservice.html'

    def get_data(self, request, context, *args, **kwargs):
        sizeentete = 0
        listeentete = []
        allServices = []
        url = 'http://iot.testnca.org:4041/iot/services'
        headers = {
                    "Fiware-Service": "",
                    "Fiware-ServicePath": "/*"
                       }
        """ Reponse de l'api """
        response = requests.get(url, headers=headers)
        """ Retourne le resultat ss forme d dictionnaire"""
        json_data = sorted(response.json().items(), key=lambda t: t[0])
        if str((json_data[0][0])) == "count":
            #la valeur de la clé services du json_data // une liste
            liste = json_data[1][1]
            for serviceitem in liste:
                nouvelleliste = sorted(serviceitem.items(), key=lambda s: s[0])
                if len(nouvelleliste) > sizeentete:
                    sizeentete = len(nouvelleliste)
                    nouvelleEntete = []
                    for ituple in nouvelleliste:
                        if ituple[0] == "apikey" or ituple[0] == "subservice" or ituple[0] == "service" or ituple[0] == "resource":
                            ituple = ituple + ("true",)
                        else:
                            ituple = ituple + ("false",)
                        nouvelleEntete.append(ituple)
                allServices.append(nouvelleliste)
        else:
            #Un seul service - une liste de tuples de services
            nouvelleliste = sorted(json_data, key=lambda x: x[0])
            sizeentete = len(nouvelleliste)
            nouvelleEntete = []
            for ituple in nouvelleliste:
                if ituple[0] == "subservice" or ituple[0] == "service":
                    ituple = ituple + ("true",)
                else:
                    ituple = ituple + ("false",)
                nouvelleEntete.append(ituple)
            allServices.append(nouvelleliste)
        context["sizeentete"] = sizeentete
        context["listeentete"] = nouvelleEntete
        context['result'] = allServices
        context['panel_name'] = 'Retrieve services'
        return context

class UpdateServiceView(views.APIView):
    tab_group_class = fiwaredashboard_tabs.FiwarepanelTabs
    template_name = 'fiwarepanel/updateservice.html'

    def get_data(self, request, context, *args, **kwargs):
        url = 'http://iot.testnca.org:4041/iot/services?apikey=API8&resource=/iot/d'
        values = """
          {
            "entity_type": "Update"
          }
        """
        headers = {
            'Content-Type': 'application/json',
            'Fiware-Service': 'portal',
            'Fiware-ServicePath': '/subservportal'
        }
        response = requests.put(url=url,  data=values, headers=headers)
        context['result'] = response.status_code
        context['panel_name'] = 'Update a service'
        return context

def newService(request):
    lazy = []
    commands = []
    attributes = []
    internal_attributes = []
    static_attributes = []
    json = {
            "_id": "",
            "subservice": "",
            "service": "",
            "apikey": "",
            "resource": "",
            "__v": 0,
            "attributes": [
                {
                    "type": "",
                    "name": "",
                    "object_id": ""
                }
            ],
            "entity_type": "Update",
        }
    form = newServiceForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # traitements à faire sur les données saisies
        pass
    template = 'fiwarepanel/newservice.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)

def testpost(request):
    template = 'fiwarepanel/testpost.html'
    #return render_to_response(template)
    context = RequestContext(request, {'context': "lhl"})
    #return render_to_response(template, context)
    return render(request, template)