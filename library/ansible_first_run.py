#!/usr/bin/python

ASNIBLE_FACTS_PATH = '/etc/ansible/facts.d'
FACT_NAME = 'ansible_first_run'

import errno
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
        supports_check_mode = True
    )

    if not module.check_mode:
        mkdir_p(ASNIBLE_FACTS_PATH)

    fact = os.path.join(ASNIBLE_FACTS_PATH, "{}.fact".format(FACT_NAME))

    changed = False
    ansible_facts = {}
    if not os.path.isfile(fact):
        if not module.check_mode:
            f = open(fact, 'w')
            f.write("false\n")
            f.close()
        changed = True
        ansible_facts = { 'ansible_local': { FACT_NAME: True } }

    module.exit_json(changed=changed, ansible_facts=ansible_facts)


from ansible.module_utils.basic import AnsibleModule
main()
