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

# Conditional imports for the various django apps that rhic-serve installs to
# see which ones are installed.
# We could use separate urls.py for each, but this seems easier for now.

try:
    from rhic_serve.rhic_rest.api import rhic
    has_rhic_rest = True
except ImportError:
    has_rhic_rest = False

try:
    from rhic_serve import rhic_webui
    has_rhic_webui = True
except ImportError:
    has_rhic_webui = False

try:
    from rhic_serve import rhic_rcs
    has_rhic_rcs = True
except ImportError:
    has_rhic_rcs = False


urlpatterns = patterns('', )

if has_rhic_rest:
    # Resources
    rhic_resource = rhic.RHICResource()
    rhic_download_resource = rhic.RHICDownloadResource()
    account_resource = rhic.AccountResource()

    urlpatterns += (
        # RHIC API Resources
        url(r'^api/', include(rhic_resource.urls)),
        url(r'^api/', include(rhic_download_resource.urls)),
        url(r'^api/', include(account_resource.urls)),
    )

if has_rhic_webui:
    urlpatterns += (
        # UI Views
        url(r'^ui/$', 'rhic_serve.rhic_webui.views.index'),
        url(r'^ui/login$', 'rhic_serve.rhic_webui.views.login'),
        url(r'^ui/logout$', 'rhic_serve.rhic_webui.views.logout'),
        url(r'^ui/rhic$', 'rhic_serve.rhic_webui.views.rhic'),
    )

if has_rhic_rcs:
    urlpatterns += (
        # RHIC RCS Resources
        url(r'^api/', include('rhic_serve.rhic_rcs.urls')),
    )


