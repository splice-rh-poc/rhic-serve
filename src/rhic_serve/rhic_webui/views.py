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

from django.contrib.auth import (login as auth_login, 
    logout as auth_logout, authenticate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

def template_response(request, template_name):
    return render_to_response(template_name, {},
        context_instance=RequestContext(request))

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return template_response(request, 'base.html')
        else:
            pass
            # Return a 'disabled account' error message
    else:
        pass
        # Return an 'invalid login' error message.    

def logout(request):
    auth_logout(request)
    return template_response(request, 'logout.html')

@ensure_csrf_cookie
def index(request):
    return template_response(request, 'base.html')

@login_required
def rhic(request):
    return template_response(request, 'rhic.html')


