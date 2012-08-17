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


from django.contrib.auth import login

class RestLoginMiddleware(object):
    """
    Middleware class to log in the authenticated user.

    Tastypie does user authentication as part of the method dispatch.
    Therefore, we have to call login() at some point so that the authenticated
    user gets saved in the session.  resposne middleware seems like a
    reasonable place to do that.
    """
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # The login() function requires that request.user.backend has been
            # set, and the only thing that sets that is
            # django.contrib.auth.authenticate().  So, effectively, we're only
            # logging in after authenticating.
            if hasattr(request.user, 'backend'):
                login(request, request.user)

        return response
