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


from rhic_rest.models import RHIC, Account, Product, Contract
from rhic_rest.api.base import RestResource, AccountAuthorization

from tastypie.authorization import Authorization
from tastypie_mongoengine.fields import (EmbeddedDocumentField,
    EmbeddedListField)

class RHICResource(RestResource):

    class Meta(RestResource.Meta):
        queryset = RHIC.objects.all()
        authorization = AccountAuthorization()

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
        bundle.data['account_id'] = bundle.request.user.username
        return bundle

class ProductResource(RestResource):

    class Meta(RestResource.Meta):
        queryset = object_class = Product

class ContractResource(RestResource):

    products = EmbeddedListField(of='rhic_rest.api.rhic.ProductResource',
        attribute='products', full=True)

    class Meta(RestResource.Meta):
        queryset = object_class = Contract

class AccountResource(RestResource):

    contracts = EmbeddedListField(of='rhic_rest.api.rhic.ContractResource', 
        attribute='contracts', full=True)

    class Meta(RestResource.Meta):
        queryset = Account.objects.all()
        authorization = AccountAuthorization()

    def dehydrate(self, bundle):
        return bundle

