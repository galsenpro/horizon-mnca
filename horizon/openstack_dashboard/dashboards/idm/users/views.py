# Copyright (C) 2014 Universidad Politecnica de Madrid
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

import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from horizon import exceptions
from horizon import forms
from horizon import tables

from openstack_dashboard import api
from openstack_dashboard import fiware_api
from openstack_dashboard.local import local_settings
from openstack_dashboard.dashboards.idm import utils as idm_utils
from openstack_dashboard.dashboards.idm import views as idm_views
from openstack_dashboard.dashboards.idm.users \
    import tables as user_tables
from openstack_dashboard.dashboards.idm.users \
    import forms as user_forms

from django_gravatar.helpers import get_gravatar_url, has_gravatar


LOG = logging.getLogger('idm_logger')
LIMIT = getattr(local_settings, 'PAGE_LIMIT', 8)
LIMIT_MINI = getattr(local_settings, 'PAGE_LIMIT_MINI', 4)


class DetailUserView(tables.MultiTableView):
    template_name = 'idm/users/index.html'
    table_classes = (user_tables.OrganizationsTable,
                     user_tables.ApplicationsTable)

    def dispatch(self, request, *args, **kwargs):
        user = kwargs['user_id']
        try:
            fiware_api.keystone.user_get(request, user)
        except Exception:
            redirect = reverse("horizon:idm:home:index")
            exceptions.handle(self.request, 
                    ('User does not exist'), redirect=redirect)
        return super(DetailUserView, self).dispatch(request, *args, **kwargs)
    
    def get_organizations_data(self):
        organizations = []
        # index_org = self.request.GET.get('index_org', 0)
        # LOG.debug(self.request.path)
        # path = self.request.path
        # user_id = path.split('/')[3]

        # #domain_context = self.request.session.get('domain_context', None)
        # try:
        #     organizations = fiware_api.keystone.project_list(
        #         self.request,
        #         user=user_id)

        #     organizations = idm_utils.filter_default(sorted(organizations, key=lambda x: x.name.lower()))
        #     organizations = idm_utils.paginate(self, organizations,
        #                                        index=index_org, limit=LIMIT_MINI,
        #                                        table_name='organizations')

        # except Exception:
        #     self._more = False
        #     exceptions.handle(self.request,
        #                       ("Unable to retrieve organization information."))
        return organizations

    def get_applications_data(self):
        applications = []
        # index_app = self.request.GET.get('index_app', 0)
        # path = self.request.path
        # user_id = path.split('/')[3]

        # try:
        #     # TODO(garcianavalon) extract to fiware_api
        #     all_apps = fiware_api.keystone.application_list(self.request)
        #     apps_with_roles = [a.application_id for a 
        #                        in fiware_api.keystone.user_role_assignments(
        #                        self.request, user=user_id)]
        #     applications = [app for app in all_apps 
        #                     if app.id in apps_with_roles]
        #     applications = idm_utils.filter_default(
        #                     sorted(applications, key=lambda x: x.name.lower()))

        #     applications = idm_utils.paginate(self, applications,
        #                                       index=index_app, limit=LIMIT_MINI,
        #                                       table_name='applications')

        # except Exception:
        #     exceptions.handle(self.request,
        #                       ("Unable to retrieve application list."))
        return applications

    def _can_edit(self):
        # Allowed if its the same user
        return (self.request.user.id == self.kwargs['user_id']
            and self.request.organization.id == self.request.user.default_project_id)

    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = fiware_api.keystone.user_get(self.request, user_id)
        user_email = getattr(user, 'name', None)
        context['user'] = user
        if getattr(user, 'use_gravatar', None) and has_gravatar(user_email):
            image = get_gravatar_url(user_email, size=idm_utils.AVATAR_SIZE['img_original'])
        elif hasattr(user, 'img_original') and getattr(user, 'img_original') != '':
            image = getattr(user, 'img_original')
            image = settings.MEDIA_URL + image
        else:
            image = settings.STATIC_URL + 'dashboard/img/logos/original/user.png'
        context['image'] = image
        context['index_app'] = self.request.GET.get('index_app', 0)
        context['index_org'] = self.request.GET.get('index_org', 0)
        if self._can_edit():
            context['edit'] = True
        return context

class BaseUsersMultiFormView(idm_views.BaseMultiFormView):
    template_name = 'idm/users/edit.html'
    forms_classes = [
        user_forms.InfoForm,
        user_forms.AvatarForm
    ]

    def _can_edit(self):
        # Allowed if its the same user
        return (self.request.user.id == self.kwargs['user_id']
            and self.request.organization.id == self.request.user.default_project_id)

    def dispatch(self, request, *args, **kwargs):
        if self._can_edit():
            return super(BaseUsersMultiFormView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('horizon:user_home')
    
    def get_endpoint(self, form_class):
        """Override to allow runtime endpoint declaration"""
        endpoints = {
            user_forms.InfoForm: reverse(
                'horizon:idm:users:info', kwargs=self.kwargs),
            user_forms.AvatarForm: reverse(
                'horizon:idm:users:avatar', kwargs=self.kwargs),
        }
        return endpoints.get(form_class)

    def get_object(self):
        try:
            return fiware_api.keystone.user_get(self.request, 
                                         self.kwargs['user_id'])
        except Exception:
            redirect = reverse("horizon:idm:home:index")
            exceptions.handle(self.request, 
                    ('Unable to update user'), redirect=redirect)

    def get_initial(self, form_class):
        initial = super(BaseUsersMultiFormView, self).get_initial(
            form_class)  
        # Existing data from organizations
        initial.update({
            "userID": self.object.id,
            "name": getattr(self.object, 'name', ''),
            "username": getattr(self.object, 'username', ''),
            "description": getattr(self.object, 'description', ''),    
            "city": getattr(self.object, 'city', ''),
            "website": getattr(self.object, 'website', ''),
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(BaseUsersMultiFormView, self).get_context_data(**kwargs)

        user_id = self.kwargs['user_id']
        context['user_id'] = user_id

        if getattr(self.object, 'use_gravatar', None):
            context['using_gravatar'] = True
        
        if has_gravatar(getattr(self.object, 'name', None)):
            gravatar_image = get_gravatar_url(getattr(self.object, 'name', None), size=idm_utils.AVATAR_SIZE['img_original'])
            context['gravatar_image'] = gravatar_image
        if hasattr(self.object, 'img_original') and getattr(self.object, 'img_original') != '':
            uploaded_image = getattr(self.object, 'img_original')
            uploaded_image = settings.MEDIA_URL + uploaded_image
        else:
            uploaded_image = (settings.STATIC_URL + 
                'dashboard/img/logos/original/user.png')
            context['no_uploaded_image'] = True
        context['uploaded_image'] = uploaded_image
        return context


class InfoFormHandleView(BaseUsersMultiFormView):    
    form_to_handle_class = user_forms.InfoForm
   
class AvatarFormHandleView(BaseUsersMultiFormView):
    form_to_handle_class = user_forms.AvatarForm

class DeleteImageView(forms.ModalFormView):
    form_class = user_forms.DeleteImageForm
    template_name = 'idm/users/delete_image.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteImageView, self).get_context_data(**kwargs)

        context['user_id'] = self.kwargs.get('user_id')
        return context

    def get_form_kwargs(self):
        kwargs = super(DeleteImageView, self).get_form_kwargs()

        kwargs.update(self.kwargs)
        return kwargs

    def dispatch(self, request, user_id, *args, **kwargs):

        user = fiware_api.keystone.user_get(self.request, user_id)

        if not hasattr(user, 'img_original') and getattr(user, 'img_original') != '':
            return redirect('horizon:idm:users:edit')
        return super(DeleteImageView, self).dispatch(request, args, kwargs)


def tour_ended(request, user_id):
    if request.is_ajax():
        fiware_api.keystone.user_update(request, request.user.id, starters_tour_ended=True, password='')

    return redirect('horizon:idm:home:index')
