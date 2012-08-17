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

from django.conf import settings

# Given all the base classes, fields, etc, that we need to make use of from
# mognoengine, it's easiest to just use import *
from mongoengine import *
from mongoengine import signals
from mongoengine.queryset import QuerySet

from rhic_rest.common import cert_utils

import uuid

class BaseQuery(object):
    """
    BaseQuery and BaseQuerySet are 2 dummy classes to work around a mongoengine
    incompatibility with tastypie.  tastypie assumes each resources model
    queryset has a query object associated with it, and that query object has
    an attribute called query_terms.

    These classes work around that assumption.
    """
    query_terms = object()


class BaseQuerySet(QuerySet):
    """
    BaseQuery and BaseQuerySet are 2 dummy classes to work around a mongoengine
    incompatibility with tastypie.  tastypie assumes each resources model
    queryset has a query object associated with it, and that query object has
    an attribute called query_terms.

    These classes work around that assumption.
    """
    def __init__(self, *args, **kwargs):
        QuerySet.__init__(self, *args, **kwargs)
        self.query = BaseQuery()


class Account(Document):
    # Unique account identifier
    account_id = StringField()
    # List of contracts associated with the account.
    contracts = ListField()


class Contract(Document):
    pass


class RHIC(Document):

    meta = {
        # Override collection name, otherwise we get r_h_i_c.
        'collection': 'rhic',
        'queryset_class': BaseQuerySet,
    }

    # Unique account identifier tying the RHIC to an account.
    account_id = StringField()
    # Contract associated with the RHIC.
    contract = StringField()
    # Support Level associated with the RHIC.
    support_level = StringField()
    # SLA (service level availability) associated with the RHIC.
    sla = StringField()
    # UUID associated with the RHIC.
    uuid = UUIDField()
    # List of Products associated with the RHIC.
    products = ListField()
    # Public cert portion of the RHIC.
    public_cert = FileField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """
        pre_save signal hook.
        """
        # Verify a UUID is always set before we save.  If one is not, generate a
        # new one and set it.
        if not document.uuid:
            document.uuid = cls._generate_uuid()

        # Generate a certificate and private key for this RHIC.
        if not document.public_cert:
            public_cert, private_key = cert_utils.generate(
                str(document.uuid), settings.CA_CERT_PATH, settings.CA_KEY_PATH,
                settings.CERT_DAYS)
            document.public_cert.new_file()
            document.public_cert.write(public_cert)
            document.public_cert.close()

            document.private_key = private_key

    @classmethod
    def _generate_uuid(cls):
        """
        Generate a random UUID.
        """
        return uuid.uuid4()


# Signals
signals.pre_save.connect(RHIC.pre_save, sender=RHIC)

