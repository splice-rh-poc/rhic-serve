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

'''
Contains functions related to working with both content and entitlement
certificates.
'''

'''
This module mostly borrowed from RHUI.
'''

import logging
import os
import shutil
import subprocess
import tempfile

from M2Crypto import X509, RSA, EVP, util

LOG = logging.getLogger(__name__)

def generate(cn, ca_cert_filename, ca_key_filename, days):
    '''
    Generates an X509 certificate

    @param cert_name: logical name of the certificate, used in the cert and key names
    @type  cert_name: str

    @param dest_dir: full path to the directory in which to store the generated cert;
                     will be created if it does not exist
    @type  dest_dir: str

    @param ca_cert_filename: full path to the CA certificate used to sign the generated cert
    @type  ca_cert_filename: str

    @param ca_key_filename: full path to the CA private key
    @type  ca_key_filename: str

    @param days: number of days the certificate should be valid for
    @type  days: int
    '''

    # Temporary working directory
    dest_dir = tempfile.mkdtemp()

    cert_name = 'rhic'

    try:
        _generate_cert_request(dest_dir, cert_name, cn)
        exit_code = _sign_request(dest_dir, cert_name, ca_cert_filename, ca_key_filename, days)
        public_cert = open(_cert_filename(dest_dir, cert_name)).read()
        private_key = open(_priv_key_filename(dest_dir, cert_name)).read()
    finally:
        shutil.rmtree(dest_dir)

    return public_cert, private_key

def _generate_cert_request(dest_dir, cert_name, cn):

    priv_key_filename = _priv_key_filename(dest_dir, cert_name)
    csr_filename = _csr_filename(dest_dir, cert_name)

    # Generate private key
    rsa = RSA.gen_key(2048, 65537)
    pk = EVP.PKey()
    pk.assign_rsa(rsa)

    pk.save_key(priv_key_filename, cipher=None, callback=util.no_passphrase_callback)

    # This is... ugh, man, this is ugly. Big surprise, M2Crypto doesn't expose a way
    # to convert PKCS8 to RSA format, so shell out to openssl to do it
    cmd = 'openssl rsa -in %s -out %s' % (priv_key_filename, priv_key_filename)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    exit_code = p.returncode
    output = p.stdout.read()
    error = p.stderr.read()

    LOG.info('Private key creation output')
    LOG.info('Exit Code: ' + str(exit_code))
    LOG.info(output)
    LOG.info(error)

    # Generate request
    request = X509.Request()
    request.set_pubkey(pk)
    request.set_version(3)

    name = request.get_subject()
    name.CN = cn

    request.sign(pk, 'sha1')

    # The RHEL 5 version of m2crypto (0.16) doesn't have the save method defined, so manually
    # write out the PEM
    # request.save(csr_file)

    f = open(csr_filename, 'w')
    f.write(request.as_pem())
    f.close()

def _sign_request(dest_dir, cert_name, ca_cert_filename, ca_key_filename, days=365):
    '''
    Signs the certificate request generated by _generate_cert_request.

    M2Crypto doesn't seem to have a way of signing a CSR with a CA certificate;
    it only looks like it supports self-signed certificates. As such, the quickest
    solution was to use a system call out to openssl directly.


    @return: exit code of the openssl process to sign the certificate request
    @rtype:  int
    '''
    csr_filename = _csr_filename(dest_dir, cert_name)
    crt_filename = _cert_filename(dest_dir, cert_name)
    ca_srl_filename = os.path.join(os.path.dirname(ca_cert_filename), 
        '%s.srl' % (os.path.basename(os.path.splitext(ca_cert_filename)[0])))

    cmd = 'openssl x509 -req -days %s -in %s -CA %s -CAkey %s -CAserial %s -out %s' % \
          (days, csr_filename, ca_cert_filename, ca_key_filename,
           ca_srl_filename, crt_filename)

    LOG.info('Command [%s]' % cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    exit_code = p.returncode
    output = p.stdout.read()
    error = p.stderr.read()

    LOG.info('Certificate creation output')
    LOG.info(output)
    LOG.info(error)

    return exit_code

def _priv_key_filename(dest_dir, cert_name):
    return os.path.join(dest_dir, '%s.key' % cert_name)

def _csr_filename(dest_dir, cert_name):
    return os.path.join(dest_dir, '%s.csr' % cert_name)

def _cert_filename(dest_dir, cert_name):
    return os.path.join(dest_dir, '%s.crt' % cert_name)
