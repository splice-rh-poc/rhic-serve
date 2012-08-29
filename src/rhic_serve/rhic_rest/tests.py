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

from django.conf import settings
from django.test import client, simple, testcases

from mongoengine import connection

from rhic_serve.rhic_rest.models import RHIC

MONGO_TEST_DATABASE_NAME = 'test_%s' % settings.MONGO_DATABASE_NAME

class MongoTestRunner(simple.DjangoTestSuiteRunner):

    def setup_databases(self, *args, **kwargs):
        # Disconnect from the default mongo db, and use a test db instead.
        connection.disconnect()
        connection.connect(MONGO_TEST_DATABASE_NAME)


    def teardown_databases(self, *args, **kwargs):
        connection.disconnect()

        # Do we want to drop the test database as well?
        # Might as well keep it around for now.
        # connection.drop_database(MONGO_TEST_DATABASE_NAME)


class MongoTestCase(testcases.TestCase):
    def _fixture_setup(self, *args, **kwargs):
        pass

    def _fixture_teardown(self, *args, **kwargs):
        pass


class RHICModelTest(MongoTestCase):
    def test_rhic_uuid_on_save(self):
        """
        Tests that a rhic gets a uuid generated when it's saved.
        """
        r = RHIC()
        r.account_id = 'test'
        r.save()
        self.assertEquals(32, len(r.uuid.hex))

