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

from rhic_serve.common.fields import *


class RHIC(Document):

    meta = {
        # Override collection name, otherwise we get r_h_i_c.
        'collection': 'rhic',
    }

    uuid = UUIDField()
    # List of Products associated with the RHIC.
    engineering_ids = ListField()
    # Date RHIC was created
    created_date = IsoDateTimeField(default=datetime.now(tzutc()))
    # Date RHIC was last modified
    modified_date = IsoDateTimeField(default=datetime.now(tzutc()))
