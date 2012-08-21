# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from django.conf.urls import patterns, include, url
from rhic_rest.api import rhic

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# Resources
rhic_resource = rhic.RHICResource()
account_resource = rhic.AccountResource()
contract_resource = rhic.ContractResource()
product_resource = rhic.ProductResource()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # API Resources
    url(r'^api/', include(rhic_resource.urls)),
    url(r'^api/', include(account_resource.urls)),
    url(r'^api/', include(contract_resource.urls)),
    url(r'^api/', include(product_resource.urls)),

    # UI Views
    url(r'^ui/$', 'rhic_webui.views.index'),
    url(r'^ui/login$', 'rhic_webui.views.login'),
    url(r'^ui/logout$', 'rhic_webui.views.logout'),
    url(r'^ui/rhic$', 'rhic_webui.views.rhic'),

)
