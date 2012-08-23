#!/usr/bin/python

import os
import sys

sys.path.insert(0, '../src/rhic_serve')

os.environ['DJANGO_SETTINGS_MODULE'] = 'rhic_serve.settings'

from rhic_serve import settings
from rhic_rest.models import *

def load_lines(lines, mappings):
    """
    Expects lines in this format:
    Login, Account#,Contract#,Marketing Product,SLA,Support Level,Number Concurrent
    """
    for line in lines:
        if line.startswith('#'):
            continue

        values = line.split(',')

        if len(values) != 7:
            print "rejecting line: %s" % line
            continue

        login, account, contract, product, sla, support_level, quantity = values

        account_doc, created = Account.objects.get_or_create(login=login, account_id=account)
        contract_ids = [c.contract_id for c in account_doc.contracts]

        if contract in contract_ids:
            contract_doc = account_doc.contracts[contract_ids.index(contract)]
        else:
            contract_doc = Contract(contract_id=contract)
            account_doc.contracts.append(contract_doc)

        sla = [s for s in Product.sla_choices if \
            Product.sla_choices[s] == sla][0]
        support_level = [s for s in Product.support_level_choices if \
            Product.support_level_choices[s] == support_level][0]

        product_doc = Product(name=product,
            engineering_id=mappings[product], sla=sla,
            support_level=support_level, quantity=quantity)

        contract_doc.products.append(product_doc)

        account_doc.save()


def load_mappings(lines):
    """
    Expects lines with this format:
    Marketing Product,Engineering Product ID,Machine Facts
    """
    mappings = {}

    for line in lines:
        if line.startswith('#'):
            continue

        values = line.split(',')

        if len(values) != 3:
            print "rejecting line: %s" % line
            continue

        product, eng_id, facts = values

        mappings[product] = eng_id

    return mappings


def main():
    file_path = sys.argv[2]
    lines = open(file_path, 'r').read().split('\n')
    mappings = load_mappings(lines)

    file_path = sys.argv[1]
    lines = open(file_path, 'r').read().split('\n')
    load_lines(lines, mappings)

if __name__ == '__main__':
    main()
