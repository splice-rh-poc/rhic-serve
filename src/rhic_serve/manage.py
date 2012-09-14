#!/usr/bin/env python
import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(curr_dir, '..'))
sys.path.insert(0, os.path.join(curr_dir, '../..'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
