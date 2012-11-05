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


from datetime import datetime
from dateutil.tz import tzutc

from django.conf import settings

# Given all the base classes, fields, etc, that we need to make use of from
# mognoengine, it's easiest to just use import *
from mongoengine import *
from mongoengine import signals
from mongoengine.base import ValidationError
from mongoengine.django.auth import User
#from django.contrib.auth.models import User
from mongoengine.queryset import QuerySet
from django.db import models

from certutils.certutils import CertUtils
from rhic_serve.common.fields import *

import uuid


class Product(EmbeddedDocument):

    support_level_choices = {
        'l1-l3': 'L1-L3',
        'l3': 'L3-only',
        'ss': 'SS',
    }

    sla_choices = {
        'std': 'Standard',
        'prem': 'Premium',
        'na': 'N/A',
    }

    # Product name
    name = StringField(required=True)
    # Unique product identifier
    engineering_ids = ListField(required=True)
    # Quantity 
    quantity = IntField(required=True)
    # Product support level
    support_level = StringField(required=True, choices=support_level_choices.keys())
    # Product sla
    sla = StringField(required=True, choices=sla_choices.keys())


class Contract(EmbeddedDocument):
    # Unique Contract identifier
    contract_id = StringField(unique=True, required=True)
    # List of products associated with this contract
    products = ListField(EmbeddedDocumentField(Product))


class Account(Document):

    meta = {
        'db_alias': 'rhic_serve'
    }

    # Unique account identifier
    account_id = StringField(unique=True, required=True)
    # Human readable account name
    login = StringField(unique=True, required=True)
    # List of contracts associated with the account.
    contracts = ListField(EmbeddedDocumentField(Contract))

class SpliceUserProfile(User):
    meta = {
        'db_alias': 'rhic_serve'
    }
    account = StringField(unique=True, required=True)

class SpliceAdminGroup(Document):
    meta = {
        'db_alias': 'rhic_serve'
    }
    name = StringField(unique=True, required=True)
    members = ListField()
    permissions = ListField()

class RHIC(Document):

    meta = {
        # Override collection name, otherwise we get r_h_i_c.
        'collection': 'rhic',
        'db_alias': 'rhic_serve'
    }

    # Human readable name
    name = StringField(unique=True, required=True)
    # Unique account identifier tying the RHIC to an account.
    account_id = StringField(required=True)
    # Contract associated with the RHIC.
    contract = StringField(required=True)
    # Support Level associated with the RHIC.
    support_level = StringField(required=True)
    # SLA (service level availability) associated with the RHIC.
    sla = StringField(required=True)
    # UUID associated with the RHIC.
    uuid = UUIDField(required=True, binary=False)
    # List of Products associated with the RHIC.
    products = ListField()
    # List of Engineering Id's associated with the RHIC.
    engineering_ids = ListField()
    # Public cert portion of the RHIC.
    public_cert = FileField(required=True)
    # Flag to indicate if this RHIC has been deleted.
    deleted = BooleanField(default=False)
    # Date RHIC was created
    created_date = IsoDateTimeField(required=True)
    # Date RHIC was last modified
    modified_date = IsoDateTimeField(required=True)
    # Date RHIC was deleted
    deleted_date = IsoDateTimeField()

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

            # Fields are validated in save(), but we need to validate
            # account_id was set here since we need to use it in the X509
            # request.
            if not document.account_id:
                raise ValidationError('account_id is not set')

            cu = CertUtils()
            public_cert, private_key = cu.generate(
                settings.CA_CERT_PATH, settings.CA_KEY_PATH,
                settings.CERT_DAYS, dict(CN=str(document.uuid),
                                         O=document.account_id))
            document.public_cert.new_file()
            document.public_cert.write(public_cert)
            document.public_cert.close()

            # private key is saved as an attribute on the document, but it is
            # not a field.  It will not be kept after this instance is GC'd.
            document.private_key = private_key

        # Created Date
        if not document.created_date:
            document.created_date = datetime.now(tzutc())

        # Modified Date.
        # This will get updated whether or not anything changed.  I guess
        # that's ok.
        document.modified_date = datetime.now(tzutc())

    @classmethod
    def _generate_uuid(cls):
        """
        Generate a random UUID.
        """
        return uuid.uuid4()


# Signals
signals.pre_save.connect(RHIC.pre_save, sender=RHIC)

