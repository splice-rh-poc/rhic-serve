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
from subprocess import call

from django.conf import settings
from django.test import client, simple, testcases

from mongoengine import connection


MONGO_TEST_DATABASE_NAME = 'test_%s' % settings.MONGO_DATABASE_NAME


class MongoTestRunner(simple.DjangoTestSuiteRunner):

    def setup_databases(self, *args, **kwargs):
        pass

    def teardown_databases(self, *args, **kwargs):
        pass


class PatchClient(client.Client):

    def patch(self, path, data={}, content_type=client.MULTIPART_CONTENT,
             **extra):
        "Construct a PATCH request."

        post_data = self._encode_data(data, content_type)

        parsed = client.urlparse(path)
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      self._get_path(parsed),
            'QUERY_STRING':   parsed[4],
            'REQUEST_METHOD': 'PATCH',
            'wsgi.input':     client.FakePayload(post_data),
        }
        r.update(extra)
        return self.request(**r)


class MongoTestCase(testcases.TestCase):

    client_class = PatchClient

    def _fixture_setup(self, *args, **kwargs):
        pass

    def _fixture_teardown(self, *args, **kwargs):
        pass

    def setUp(self):
        self.teardown_database()
        self.setup_database()
        super(MongoTestCase, self).setUp()

    def tearDown(self):
        self.teardown_database()
        super(MongoTestCase, self).tearDown()

    def setup_database(self, *args, **kwargs):
        # Disconnect from the default mongo db, and use a test db instead.
        connection.disconnect()
        connection.connect(MONGO_TEST_DATABASE_NAME)

        for collection in ['account', 'user', 'rhic', 'fs.chunks',
            'fs.files']:
            print 'importing %s collection' % collection
            call(['mongoimport', '--db', MONGO_TEST_DATABASE_NAME,
                '-c', collection, '--file', 
                '%s.json' % os.path.join(settings.DUMP_DIR, collection)])

    def teardown_database(self, *args, **kwargs):
        connection.disconnect()

        # Drop the test database
        pymongo_connection = connection.get_connection()
        pymongo_connection.drop_database(MONGO_TEST_DATABASE_NAME)



