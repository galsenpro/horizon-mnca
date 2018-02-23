# The name of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'fiwaredashboard'

# If set to True, this dashboard will not be added to the settings.
DISABLED = False

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.fiwaredashboard',
    'widget_tweaks',
    'django_json_widget',
    'crispy_forms',
]
