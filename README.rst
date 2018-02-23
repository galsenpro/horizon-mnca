=============================
Horizon (OpenStack Dashboard)
=============================

Horizon is a Django-based project aimed at providing a complete OpenStack
Dashboard along with an extensible framework for building new dashboards
from reusable components. The ``openstack_dashboard`` module is a reference
implementation of a Django site that uses the ``horizon`` app to provide
web-based interactions with the various OpenStack projects.

* Release management: https://launchpad.net/horizon
* Blueprints and feature specifications: https://blueprints.launchpad.net/horizon
* Issue tracking: https://bugs.launchpad.net/horizon

.. image:: https://governance.openstack.org/tc/badges/horizon.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

Using Horizon
=============

See ``doc/source/install/index.rst`` about how to install Horizon
in your OpenStack setup. It describes the example steps and
has pointers for more detailed settings and configurations.

It is also available at
`Installation Guide <https://docs.openstack.org/horizon/latest/install/index.html>`_.

Getting Started for Developers
==============================

``doc/source/quickstart.rst`` or
`Quickstart Guide <https://docs.openstack.org/horizon/latest/contributor/quickstart.html>`_
describes how to setup Horizon development environment and start development.

Create a skeleton dashboard with panel for horizon as a plugin
----------------------------------------------------------------

 - ``python setupdash dashboardname panelname panelgroupname``
 - Your dashboard + panel is ready!


How to install your panel?
---------------------------

You have two options:

 - ``python setup.py install``
  - This installs the panel on the local machine, be sure to install it where you have installed horizon!
 - Create a pypi package of your new dashboard and then install it on your horizon machine



options
--------

positional | explanation
------------- | -------------
dashboard | Dashboard name
panel | Panel name
groupname | Group name


optional | explanation
------------- | -------------
-h, --help | show this help message and exit
--dashboard-slug DASHBOARD_SLUG | Dashboard slug to use, defaults to the name
--panel-slug PANEL_SLUG | Panel slug to use, defaults to the name

