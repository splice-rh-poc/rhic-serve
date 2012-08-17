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

"""
This module currently unused.  Keeping it around as a way to show how to set
user.backend every time a user is loaded from a saved session if we choose to
do that later.  That way you can call login() in again.
"""

from mongoengine.django.auth import MongoEngineBackend

class MyBackend(MongoEngineBackend):

    def get_user(self, user_id):
        user = MongoEngineBackend.get_user(self, user_id)
        user.backend = 'rhic_rest.auth.MyBackend'
        return user

