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

class RHIC(Document):
    account_id = StringField()
    contracts = ListField()
    support_level = StringField()
    sla = StringField()
    products = ListField()

