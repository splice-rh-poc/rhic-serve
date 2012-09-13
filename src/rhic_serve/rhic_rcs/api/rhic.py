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


from rhic_serve.common.api import RestResource, AccountAuthorization
from rhic_serve.rhic_rcs.models import RHIC

from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization


class RHICRcsResource(RestResource):

    class Meta:
        queryset = RHIC.objects.all()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        detail_uri_name = 'uuid'
        fields = ['uuid', 'engineering_ids', 'resource_uri',]

