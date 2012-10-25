RHIC REST
=========

.. toctree::
   :maxdepth: 2

.. http:get:: /api/v1/rhic/

   The rhic's in the system for which the user is authorized.

   **Sample request**:

   .. sourcecode:: http

      GET /api/v1/rhic/ HTTP/1.1
      Host: example.com
      Accept: application/json

   **Sample Response**:

   .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json

      [
         {
             "account_id": "1190457", 
             "contract": "3116649", 
             "created_date": "2012-10-04T21:25:20.698000+00:00", 
             "deleted": false, 
             "deleted_date": null, 
             "engineering_ids": [
                 "69", 
                 "183"
             ], 
             "id": "506dfec0d046c81fd61eebe7", 
             "modified_date": "2012-10-04T21:25:20.698000+00:00", 
             "name": "rhel-server-jboss-1190457-3116649-prem-l1-l3", 
             "products": [
                 "RHEL Server", 
                 "JBoss EAP"
             ], 
             "public_cert": null, 
             "resource_uri": "http://localhost:8000/api/v1/rhic/fea363f5-af37-4a23-a2fd-bea8d1fff9e8/", 
             "sla": "prem", 
             "support_level": "l1-l3", 
             "uuid": "fea363f5-af37-4a23-a2fd-bea8d1fff9e8"
         }, 
         {
             "account_id": "1190457", 
             "contract": "3879847", 
             "created_date": "2012-10-04T21:25:21.138000+00:00", 
             "deleted": false, 
             "deleted_date": null, 
             "engineering_ids": [
                 "69"
             ], 
             "id": "506dfec1d046c81fd61eebea", 
             "modified_date": "2012-10-04T21:25:21.138000+00:00", 
             "name": "rhel-server-education-1190457-3879847-na-ss", 
             "products": [
                 "RHEL Server for Education"
             ], 
             "public_cert": null, 
             "resource_uri": "http://localhost:8000/api/v1/rhic/fbbd06c6-ebed-4892-87a3-2bf17c86e610/", 
             "sla": "na", 
             "support_level": "ss", 
             "uuid": "fbbd06c6-ebed-4892-87a3-2bf17c86e610"
         }
      ]

   :statuscode 200: no error

