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

from tastypie.authentication import (BasicAuthentication, 
    MultiAuthentication, SessionAuthentication)
from tastypie.authorization import Authorization
from tastypie_mongoengine.resources import MongoEngineResource

class RestResource(MongoEngineResource):
    """
    Base class for the rhic_rest application.

    Will override some functionality from MongoEngineResource.
    """

    class Meta:
        """
        Common base Rest Resource options.
        """
        # Make sure we always get back the representation of the resource back
        # on a POST.
        always_return_data = True

        # All Resources require basic authentication (for now).
        authentication = MultiAuthentication(SessionAuthentication(),
            BasicAuthentication())

    def alter_list_data_to_serialize(self, request, data):
        """
        While the meta dictionary in the standard MongoEngineResource is
        valuable for things like pagination, counts, etc., we just want the
        standard response to be the list of resources requested.

        TODO:
        We need to make the information in meta available on demand via a query
        parameter.

        This method removes a meta key from the data dictionary, and turns data
        into a list of resources.
        """
        if isinstance(data, dict):
            if 'meta' in data:
                data.pop('meta')
            if 'objects' in data:
                data = data['objects']

        return data


class RHICAuthorization(Authorization):

    def is_authorized(self, request, rhic=None):
        """
        Check if the user is authorized to see the given RHIC.

        If a specific RHIC is not being requested, just return True, and RHIC's
        the user is not authorized to see will be filtered out in apply_limits.
        """
        if rhic and rhic.account_id != request.user.username:
            return False

        return True

    def apply_limits(self, request, rhics):
        """
        Filter out all rhics that the logged in user is not authorized to see.
        """
        return rhics.filter(account_id=request.user.username)
