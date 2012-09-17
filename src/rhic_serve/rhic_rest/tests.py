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

from mongoengine.base import ValidationError

from rhic_serve.common.tests import MongoTestCase
from rhic_serve.rhic_rest.models import RHIC


class RHICModelTest(MongoTestCase):
    def test_rhic_uuid_on_save(self):
        """
        Tests that a rhic gets a uuid generated when it's saved.
        """
        r = RHIC()
        r.account_id = 'test_account'
        r.contract = 'test_contract'
        r.sla = 'test_sla'
        r.support_level = 'test_support_level'
        r.name = 'test_name'
        r.products = ['foo']
        r.engineering_ids = ['69']
        r.save()
        self.assertEquals(32, len(r.uuid.hex))

    def test_required_fields(self):
        """
        Tests that an exception is thrown if a required field is not set.
        """
        required_fields = [
            'name',
            'sla',
            'support_level',
            'uuid',
            'contract',
            'account_id',
        ]

        r = RHIC()

        for required_field in required_fields:
            self.assertRaises(ValidationError, r.save)
            setattr(r, required_field, 'test_%s' % required_field)


class RHICApiTest(MongoTestCase):

    create_rhic_json = """\
{
	"account_id" : "1190457",
	"contract" : "3116649",
	"engineering_ids" : [
		"69",
		"83"
	],
	"name" : "jj",
	"products" : [
		"RHEL Server",
		"RHEL HA"
	],
	"sla" : "prem",
	"support_level" : "l1-l3"
}
"""

    patch_rhic_json = """\
{
    "engineering_ids": ["69", "83"],
	"products" : [
		"RHEL Server",
		"RHEL HA"
	]
}
"""

    def login(self):
        self.client.login(username='shadowman@redhat.com',
            password='shadowman@redhat.com')

    def post(self, url, data):
        self.login()
        content_type = 'application/json'
        response = self.client.post(url, data, content_type)
        self.assertEquals(response.status_code, 201)
        self.client.logout()
        return response

    def get(self, url):
        self.login()
        content_type = 'application/json'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.client.logout()
        return response

    def delete(self, url):
        self.login()
        content_type = 'application/json'
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)
        self.client.logout()
        return response

    def patch(self, url, data):
        self.login()
        content_type = 'application/json'
        response = self.client.patch(url, data, content_type)
        self.assertEquals(response.status_code, 202)
        self.client.logout()
        return response

    def test_create_rhic(self):
        """
        Create RHIC Test.
        """
        response = self.post('/api/rhic/', self.create_rhic_json)
        json = response.content
        rhic = simplejson.loads(json)
        self.assertEquals('jj-1190457-3116649-prem-l1-l3', rhic['name'])
        self.assertEquals('1190457', rhic['account_id'])
        self.assertEquals('prem', rhic['sla'])
        self.assertEquals('l1-l3', rhic['support_level'])
        self.assertEquals('3116649', rhic['contract'])
        self.assertEquals(['69', '83'], rhic['engineering_ids'])
        self.assertEquals(['RHEL Server', 'RHEL HA'], rhic['products'])
        self.assertEquals(36, len(rhic['uuid']))
        self.assertEquals('http://testserver/api/rhic/%s/' % rhic['uuid'],
            rhic['resource_uri'])

        # Just test that something got generated for these.
        self.assertGreater(len(rhic['private_key']), 100)
        self.assertGreater(len(rhic['public_cert']), 100)
        self.assertGreater(len(rhic['cert_pem']), 100)

    def test_patch_rhic(self):
        """
        Patch (update) RHIC Test.
        """
        response = self.patch(
            '/api/rhic/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/', 
            self.patch_rhic_json)
        json = response.content
        rhic = simplejson.loads(json)
        self.assertEquals(rhic['engineering_ids'], ['69', '83'])

    def test_get_rhics(self):
        """
        Get all rhics.
        """
        response = self.get('/api/rhic/')
        json = response.content
        rhics = simplejson.loads(json)
        self.assertEquals(8, len(rhics))

    def test_get_rhic(self):
        response = self.get('/api/rhic/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/')
        json = response.content
        rhic = simplejson.loads(json)
        self.assertIsInstance(rhic, dict)
        self.assertEquals('ed74e2a5-eb37-4bcb-9504-a9c338db56d0', rhic['uuid'])

    def test_delete_rhic(self):
        """
        Delete RHIC Test.
        """
        response = self.delete('/api/rhic/ed74e2a5-eb37-4bcb-9504-a9c338db56d0/')

        response = self.get('/api/rhic/')
        json = response.content
        rhics = simplejson.loads(json)
        self.assertEquals(7, len(rhics))


