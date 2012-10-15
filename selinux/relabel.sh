#!/bin/sh

/sbin/restorecon -R /etc/httpd/conf.d/rhic-serve.conf
/sbin/restorecon -R /etc/pki/rhic-serve
/sbin/restorecon -R /srv/rhic-serve/webservices.wsgi


