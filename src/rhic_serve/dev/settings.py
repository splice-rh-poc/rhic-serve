# Development settings

import os

from splice.common import config

SPLICE_CONFIG_FILE = 'dev/splice.conf'
config.init(SPLICE_CONFIG_FILE)

from rhic_serve.settings import *


curr_dir = os.path.dirname(os.path.abspath(__file__))
cert_dir = os.path.join(curr_dir, '../../..')

srl_path = os.path.join(cert_dir, 'etc/pki/rhic-serve/rhic-serve-ca.srl')

if not os.path.exists(srl_path):
    open(srl_path, 'w').write('01\n')

DUMP_DIR = os.path.join(curr_dir, 'db_dump')
