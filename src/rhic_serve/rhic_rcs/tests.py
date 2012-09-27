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


    def test_get_rhics(self):
        """
        Get all rhics.
        """
        response = self.get('/api/v1/rhicrcs/')
        json = response.content
        rhics = simplejson.loads(json)['objects']
        self.assertEquals(8, len(rhics))

    def test_get_rhic(self):
        response = self.get('/api/v1/rhicrcs/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/')
        json = response.content
        rhic = simplejson.loads(json)
        self.assertIsInstance(rhic, dict)
        self.assertEquals('ed74e2a5-eb37-4bcb-9504-a9c338db56d0', rhic['uuid'])

    def test_get_deleted_rhics(self):

        # 1 rhic is already deleted in the sample data
        response = self.get('/api/v1/rhicrcs/?deleted__exact=True')
        json = response.content
        rhics = simplejson.loads(json)['objects']
        self.assertEquals(1, len(rhics))

        # Delete 2 more rhics
        self.delete('/api/v1/rhic/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/')
        self.delete('/api/v1/rhic/01720e7a-14d0-4a30-9ea9-de11c50c1d31/')

        # Should only be 6 non-deleted rhics left
        response = self.get('/api/v1/rhicrcs/')
        json = response.content
        rhics = simplejson.loads(json)['objects']
        self.assertEquals(6, len(rhics))
        non_deleted_uuids = [r['uuid'] for r in rhics]
        self.assertTrue('ed74e2a5-eb37-4bcb-9504-a9c338db56d0' not in 
            non_deleted_uuids)
        self.assertTrue('01720e7a-14d0-4a30-9ea9-de11c50c1d31' not in
            non_deleted_uuids)

        # 3 rhics deleted in total
        response = self.get('/api/v1/rhicrcs/?deleted__exact=True')
        json = response.content
        rhics = simplejson.loads(json)['objects']
        self.assertEquals(3, len(rhics))


    def test_get_modified_rhics(self):

        response = self.get(
            '/api/v1/rhicrcs/?modified_date__gt=2012-09-14T21:50Z')
        json = response.content
        rhics = simplejson.loads(json)
        self.assertEquals(2, len(rhics))

        # Modify a rhic
        response = self.patch(
            '/api/v1/rhic/47decdb7-d2eb-4918-b28c-0c5f57de8c19/',
            '{"engineering_ids": ["69", "83"]}')

        # Should now be 3 modified rhics greater than our query date.
        response = self.get(
            '/api/v1/rhicrcs/?modified_date__gt=2012-09-14T21:50Z')
        json = response.content
        rhics = simplejson.loads(json)['objects']
        self.assertEquals(3, len(rhics))



