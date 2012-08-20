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
import sys

sys.path.insert(0, '../src/rhic_serve')

os.environ['DJANGO_SETTINGS_MODULE'] = 'rhic_serve.settings'

from mongoengine.django.auth import User

from rhic_serve import settings
from rhic_rest.models import *

User.objects.all().delete()
Account.objects.all().delete()
RHIC.objects.all().delete()
