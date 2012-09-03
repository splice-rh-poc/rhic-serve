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


import sys
import urllib

from django.http import HttpResponse

from rhic_serve.rhic_rest.models import RHIC, Account, Product, Contract
from rhic_serve.rhic_rest.api.base import RestResource, AccountAuthorization

from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie_mongoengine.fields import (EmbeddedDocumentField,
    EmbeddedListField)
from tastypie.validation import Validation

class RHICValidation(Validation):

    def is_valid(self, bundle, request=None):
        valid = super(RHICValidation, self).is_valid(bundle, request)
        rhic = bundle.obj
        return valid


class RHICResource(RestResource):

    class Meta(RestResource.Meta):
        queryset = RHIC.objects.all()
        authorization = AccountAuthorization()
        validation = RHICValidation()
        detail_uri_name = 'uuid'

    def dehydrate_public_cert(self, bundle):
        """
        Convert public cert field (FileField using GridFS) into the actual
        string of the public cert of this RHIC.
        """
        if bundle.obj.public_cert:
            return bundle.obj.public_cert.read()
        else:
            return None
    
    def dehydrate(self, bundle):
        """
        Private key isn't stored as a field on the document, but if it's set as
        an attribute, then we just created the cert/key pair for this RHIC.
        Return the contents of the private key, and cert and key concatenated
        together in PEM format.
        """
        if hasattr(bundle.obj, 'private_key'):
            if bundle.obj.private_key:
                bundle.data['private_key'] = bundle.obj.private_key
                bundle.data['cert_pem'] = (bundle.data['public_cert'] +
                    bundle.data['private_key'])

        return bundle

    def hydrate_account_id(self, bundle):
        # Probably need to raise an error if these don't match to being with.
        account_id = Account.objects(
            login=bundle.request.user.username).only('account_id').first().account_id
        bundle.data['account_id'] = account_id
        return bundle

    def hydrate_name(self, bundle):
        bundle = self.hydrate_account_id(bundle)
        name_suffix = '%s-%s-%s-%s' % (bundle.data['account_id'],
                bundle.data['contract'], bundle.data['sla'],
                bundle.data['support_level'])
        name = bundle.data.get('name', '')
        if not name.endswith(name_suffix):
            name = '%s-%s' % (name, name_suffix)
            bundle.data['name'] = name
        return bundle

    def obj_create(self, bundle, request, **kwargs):
        """
        Fixups and protections for new RHIC creation.
        """
        return super(RHICResource, self).obj_create(bundle, request, **kwargs)


class RHICDownloadResource(RHICResource):


    def deserialize(self, request, data, format='application/json'):
        if format == "application/x-www-form-urlencoded":
            deserialized = request.POST
        elif format == "multipart/form-data":
            deserialized = request.POST.copy()
            deserialized.update(request.FILES)
        else:
            deserialized = self._meta.serializer.deserialize(data, format=format)
        
        return deserialized    
    
    def create_response(self, request, bundle, *args, **kwargs):

        if type(bundle) == type([]):
            return super(RHICDownloadResource, self).create_response(request,
                bundle, *args, **kwargs)

        cert_pem = request.GET.get('cert_pem', None)

        if cert_pem:
            cert_pem = urllib.unquote(cert_pem)
        else:
            cert_pem = bundle.data['public_cert']

        response = HttpResponse(cert_pem, content_type='test/pem')
        response['Content-Disposition'] = 'attachment; filename=%s.pem' % \
            bundle.data['uuid']
        response['Content-Length'] = sys.getsizeof(cert_pem)

        return response


class RHICRcsResource(RHICResource):

    class Meta(RHICResource.Meta):
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        fields = ['uuid', 'engineering_ids']


class ProductResource(RestResource):

    class Meta(RestResource.Meta):
        queryset = object_class = Product


class ContractResource(RestResource):

    products = EmbeddedListField(of='rhic_serve.rhic_rest.api.rhic.ProductResource',
        attribute='products', full=True)

    class Meta(RestResource.Meta):
        queryset = object_class = Contract


class AccountResource(RestResource):

    contracts = EmbeddedListField(of='rhic_serve.rhic_rest.api.rhic.ContractResource', 
        attribute='contracts', full=True)

    class Meta(RestResource.Meta):
        queryset = Account.objects.all()
        authorization = AccountAuthorization()

    def dehydrate(self, bundle):
        return bundle

