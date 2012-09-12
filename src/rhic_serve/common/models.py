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


from mongoengine.queryset import QuerySet


class BaseQuery(object):
    """
    BaseQuery and BaseQuerySet are 2 dummy classes to work around a mongoengine
    incompatibility with tastypie.  tastypie assumes each resources model
    queryset has a query object associated with it, and that query object has
    an attribute called query_terms.

    These classes work around that assumption.
    """
    query_terms = object()


class BaseQuerySet(QuerySet):
    """
    BaseQuery and BaseQuerySet are 2 dummy classes to work around a mongoengine
    incompatibility with tastypie.  tastypie assumes each resources model
    queryset has a query object associated with it, and that query object has
    an attribute called query_terms.

    These classes work around that assumption.
    """
    def __init__(self, *args, **kwargs):
        QuerySet.__init__(self, *args, **kwargs)
        self.query = BaseQuery()



