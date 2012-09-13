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
from rhic_serve.rhic_rest.api import rhic


# Resources
rhic_resource = rhic.RHICResource()
rhic_download_resource = rhic.RHICDownloadResource()
account_resource = rhic.AccountResource()

urlpatterns = patterns('',

    # RHIC API Resources
    url(r'^api/', include(rhic_resource.urls)),
    url(r'^api/', include(rhic_download_resource.urls)),
    url(r'^api/', include(account_resource.urls)),

    # UI Views
    url(r'^ui/$', 'rhic_serve.rhic_webui.views.index'),
    url(r'^ui/login$', 'rhic_serve.rhic_webui.views.login'),
    url(r'^ui/logout$', 'rhic_serve.rhic_webui.views.logout'),
    url(r'^ui/rhic$', 'rhic_serve.rhic_webui.views.rhic'),

    # RHIC RCS Resources
    url(r'^api/', include('rhic_serve.rhic_rcs.urls')),

)

