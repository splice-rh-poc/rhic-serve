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

from rhic_serve.rhic_rest.models import Account

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

    def dehydrate_resource_uri(self, bundle):
        """
        Override all resource uri's with their absolute (protocol, host, port,
        path) counterparts.
        """
        resource_uri = super(RestResource, self).dehydrate_resource_uri(bundle)
        return bundle.request.build_absolute_uri(resource_uri)

    def determine_format(self, request):
        """
        Always return json.  Makes it such that sepcifying the format=json
        query parameter is not required as it typically is by tastypie.
        """
        return 'application/json'

class AccountAuthorization(Authorization):
    """
    Authorization base class that can be re-used by any resource that wants to
    authorize or deny access based on the fact that resource.account_id matches
    the logged in user's username.
    """

    def is_authorized(self, request, resource=None):
        """
        Check if the user is authorized to see the given RHIC.

        If a specific RHIC is not being requested, just return True, and RHIC's
        the user is not authorized to see will be filtered out in apply_limits.
        """
        if resource and resource.account_id != request.user.username:
            return False

        return True

    def apply_limits(self, request, resources):
        """
        Filter out all rhics that the logged in user is not authorized to see.
        """
        if request.user.username:
            account_id = Account.objects(
                login=request.user.username).only('account_id').first().account_id
            return resources.filter(account_id=account_id)
        else:
            return []
