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


import simplejson

from rhic_serve.common.tests import MongoTestCase, MongoApiTestCase


class RHICRcsApiTest(MongoApiTestCase):


    def test_get_rhicsrcs(self):
        """
        Get all rhics.
        """
        response = self.get('/api/rhic/')
        json = response.content
        rhics = simplejson.loads(json)
        self.assertEquals(8, len(rhics))

    def test_get_rhicrcs(self):
        response = self.get('/api/rhic/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/')
        json = response.content
        rhic = simplejson.loads(json)
        self.assertIsInstance(rhic, dict)
        self.assertEquals('ed74e2a5-eb37-4bcb-9504-a9c338db56d0', rhic['uuid'])
