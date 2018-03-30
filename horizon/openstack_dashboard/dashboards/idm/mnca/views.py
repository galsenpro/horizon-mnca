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
from openstack_dashboard.dashboards.idm.mnca  import tabs as idm_tabs
import requests
from rest_framework.response import Response
from rest_framework import viewsets, status
from . import serializers
from . import Service

services = {
    1: Service(id=1, service='nca', subservice='subnca', resource='/iot/d')
}

"""    Retrieves services """
class ServicesIdasView(views.APIView):
    tab_group_class = idm_tabs.MncaTabs
    template_name = 'mnca/services.html'
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
                        if ituple[0] == "subservice" or ituple[0] == "service" or ituple[0] == "resource":
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
        context['panel_name'] = 'MNCA'
        return context

def get_next_service_id():
    return max(services) + 1


class serviceViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.serviceSerializer

    def list(self, request):
        serializer = serializers.serviceSerializer(
            instance=services.values(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.serviceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            service.id = get_next_service_id()
            services[service.id] = service
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            service = services[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.serviceSerializer(instance=service)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            service = services[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.serviceSerializer(
            data=request.data, instance=service)
        if serializer.is_valid():
            service = serializer.save()
            services[service.id] = service
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            service = services[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.serviceSerializer(
            data=request.data,
            instance=service,
            partial=True)
        if serializer.is_valid():
            service = serializer.save()
            services[service.id] = service
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            service = services[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del services[service.id]
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateServiceView(views.APIView):
    tab_group_class = idm_tabs.MncaTabs
    template_name = 'mnca/updateservice.html'

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