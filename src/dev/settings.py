# Development settings

import os

from rhic_serve.settings import *

curr_dir = os.path.dirname(os.path.abspath(__file__))
cert_dir = os.path.join(curr_dir, '../..')

CA_CERT_PATH = os.path.join(cert_dir, 'etc/pki/rhic-serve/rhic-serve-ca.crt')
CA_KEY_PATH = os.path.join(cert_dir, 'etc/pki/rhic-serve/rhic-serve-ca.key')
