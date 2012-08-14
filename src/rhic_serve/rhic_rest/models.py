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

# Given all the base classes, fields, etc, that we need to make use of from
# mognoengine, it's easiest to just use import *
from mongoengine import *

import uuid

class Account(Document):
    # Unique account identifier
    account_id = StringField()
    # List of contracts associated with the account.
    contracts = ListField()


class RHIC(Document):

    meta = {
        # Override collection name, otherwise we get r_h_i_c.
        'collection': 'rhic',
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
    public_cert = StringField()
    # Private key portion of the RHIC.
    private_key = StringField()

    def save(self, *args, **kwargs):
        """
        Verify a UUID is always set before we save.  If one is not, generate a
        new one and set it.
        """
        if not self.uuid:
            self.uuid = self._generate_uuid()
        Document.save(self, *args, **kwargs)

    def _generate_uuid(self):
        """
        Generate a random UUID.
        """
        return uuid.uuid4()

