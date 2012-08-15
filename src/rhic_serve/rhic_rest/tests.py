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

from django.test import client, simple, testcases

from rhic_rest.models import RHIC

class MongoTestRunner(simple.DjangoTestSuiteRunner):

    def setup_databases(self, *args, **kwargs):
        pass

    def teardown_databases(self, *args, **kwargs):
        pass

    def _fixture_setup(self, *args, **kwargs):
        pass

    def _fixture_teardown(self, *args, **kwargs):
        pass

class MongoTestCase(testcases.TestCase):
    def _fixture_setup(self, *args, **kwargs):
        pass

    def _fixture_teardown(self, *args, **kwargs):
        pass


class RHICTest(MongoTestCase):
    def test_rhic_uuid_on_save(self):
        """
        Tests that a rhic gets a uuid generated when it's saved.
        """
        r = RHIC()
        r.account_id = 'test'
        r.save()
        self.assertEquals(32, len(r.uuid.hex))

