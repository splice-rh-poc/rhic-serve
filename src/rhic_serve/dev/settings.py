# Development settings

import os

from splice.common import config

curr_dir = os.path.dirname(__file__)
source_dir = os.path.join(curr_dir, '..')
cert_dir = os.path.join(curr_dir, '../../..')
os.chdir(source_dir)
srl_path = os.path.join(cert_dir, 'etc/pki/rhic-serve/rhic-serve-ca.srl')

# Reset configuration object just in case
config_file = os.path.join(curr_dir, 'splice.conf')
config.init(config_file, reinit=True)

from rhic_serve.settings import *

if not os.path.exists(srl_path):
    open(srl_path, 'w').write('01\n')

DUMP_DIR = os.path.join(curr_dir, 'db_dump')