# Copyright (C) 2016 Universidad Politecnica de Madrid
#
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

from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.endpoints_management.endpoints_management import views


urlpatterns = patterns('',
    url(r'^$', views.ManageEndpointsView.as_view(), name='index'),
    url(r'^(?P<service_name>[^/]+)$', views.ManageEndpointsView.as_view(), name='service'),
    url(r'^(?P<service_name>[^/]+)/edit$', views.UpdateEndpointsView.as_view(), name='edit_service'),
    url(r'^(?P<service_name>[^/]+)/disable$', views.disable_service_view, name='disable_service'),
    url(r'^(?P<service_name>[^/]+)/reset$', views.reset_service_password_view, name='reset_service'),
)
