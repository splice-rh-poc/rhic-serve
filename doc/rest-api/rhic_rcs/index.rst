RHIC RCS
========

.. toctree::
   :maxdepth: 2

.. http:get:: /api/v1/rhicrcs/

   All rhic's available to be sync'd by an RCS.

   **Sample Request**:

   .. sourcecode:: http
      
      GET /api/v1/rhicrcs/ HTTP/1.1
      Host: example.com
      Accept: application/json

   **Sample Response**:

   .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json

      [
        {
          "created_date": "2012-09-14T19:33:54.294000+00:00",
          "deleted": false,
          "deleted_date": null,
          "engineering_ids": [
            "69",
            "183"
          ],
          "id": "505386a2d9c1417e41000002",
          "modified_date": "2012-09-14T19:33:54.294000+00:00",
          "resource_uri": "https://ec2-184-72-159-16.compute-1.amazonaws.com/api/rhicrcs/7dd72d62-fcf2-4e5c-a659-273bb88bd509/",
          "uuid": "7dd72d62-fcf2-4e5c-a659-273bb88bd509"
        },
        {
          "created_date": "2012-09-14T21:04:27.090000+00:00",
          "deleted": false,
          "deleted_date": null,
          "engineering_ids": [
            "69",
            "83"
          ],
          "id": "50539bdbd9c1417e42000002",
          "modified_date": "2012-09-14T21:04:27.090000+00:00",
          "resource_uri": "https://ec2-184-72-159-16.compute-1.amazonaws.com/api/rhicrcs/5e6a8a78-ceb9-4835-80c8-4b2b337ebec4/",
          "uuid": "5e6a8a78-ceb9-4835-80c8-4b2b337ebec4"
        },
        {
          "created_date": "2012-09-14T21:13:48.752000+00:00",
          "deleted": false,
          "deleted_date": null,
          "engineering_ids": [
            "69"
          ],
          "id": "50539e0cd9c1417f38000002",
          "modified_date": "2012-09-14T21:13:48.752000+00:00",
          "resource_uri": "https://ec2-184-72-159-16.compute-1.amazonaws.com/api/rhicrcs/cc11f76f-8f82-433f-bc37-c61b5bf43d19/",
          "uuid": "cc11f76f-8f82-433f-bc37-c61b5bf43d19"
        }
      ]
      
   :query deleted: Boolean flag indicating if the rhic has been deleted.
   :query modified_date: Date rhic was last modified.
   :query created_date: Date rhic was created.
   :query deletd_date: Date rhic was deleted.
   :statuscode 200: no error
