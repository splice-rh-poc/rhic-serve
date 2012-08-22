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


import os
import random
import sys

sys.path.insert(0, '../src/rhic_serve')

os.environ['DJANGO_SETTINGS_MODULE'] = 'rhic_serve.settings'

from mongoengine.django.auth import User

from rhic_serve import settings
from rhic_rest.models import *


# sample produts
# [(sku, product name), ...]
products = [
    ('RH00001', 'Red Hat Enterprise Linux'),
    ('RH00002', 'Red Hat Enterprise Linux for Academia'),
    ('RH00003', 'Red Hat Enterprise Linux for Developers'),
    ('RH00004', 'Red Hat Enterprise MRG'),
    ('RH00005', 'Red Hat Enterprise High Availability'),
    ('RH00006', 'Red Hat Enterprise Load Balancing'),
    ('RH00007', 'Red Hat JBoss AS'),
    ('RH00008', 'Red Hat JBoss WS'),
    ('RH00009', 'Red Hat Database'),
    ('RH000010', 'Red Hat Cloudforms'),
]

# sample accounts
# [ (email, name), ...]
accounts = [
    ('optimus', 'Optimus Prime'),
    ('megatron', 'Megatron'),
    ('soundwave', 'Soundwave'),
    ('wheeljack', 'Wheeljack'),
    ('shadowman', 'Shadowman'),
]

# sample support levels
support_levels = Contract.support_level_choices.keys()

# sample sla's
slas = Contract.sla_choices.keys()

# Random number shortcut
def r(m):
    return int(random.random() * m)

# generate and save the data
for account in accounts:
    a = Account(account_id=account[0], name=account[1])

    # Create between 1 and 5 random contracts
    for i in range(1, r(5)+2):
        c = Contract(contract_id='contract-%s' % (i))

        # Associate a random sla with the contract
        c.slas = slas

        # Associate a random support level with the contract
        c.support_levels = support_levels

        # Associate between 1 and len(products) # of products
        for j in range(1, r(len(products))+2):
            # Choose a random product
            p_index = r(len(products))
            p = Product(sku=products[p_index][0], name=products[p_index][1])
            # Append the product to the contract
            c.products.append(p)

        # Append the contract to the account
        a.contracts.append(c)
        a.save()

    # generate between 1 and 3 rhics for each account
    for k in range(r(3)+1):
        c_index = r(len(a.contracts))
        c = a.contracts[c_index]
        rhic = RHIC(account_id=a.account_id, contract=c.contract_id, support_level=c.support_levels[0],
            sla=c.slas[0])
        for p_id in c.products:
            if r(2) > 0:
                rhic.products.append(p_id.sku)
        rhic.save()

    # Also create a user for each account
    u = User(username=a.account_id, first_name=a.name)
    u.set_password(a.account_id)
    u.save()

    a.save()

