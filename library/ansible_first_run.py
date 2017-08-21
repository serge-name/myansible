#!/usr/bin/python

ASNIBLE_FACTS_PATH = '/etc/ansible/facts.d'
FACT_NAME = 'ansible_first_run'

import errno
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
        return True
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return False
        else:
            raise


def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
        supports_check_mode = True
    )


    changed = False if module.check_mode else mkdir_p(ASNIBLE_FACTS_PATH)
    fact_path = os.path.join(ASNIBLE_FACTS_PATH, "{}.fact".format(FACT_NAME))
    ansible_facts = {}

    if not os.path.isfile(fact_path):
        if not module.check_mode:
            f = open(fact_path, 'w')
            f.write("false\n")
            f.close()
        changed = True
        ansible_facts = { 'ansible_local': { FACT_NAME: True } }

    module.exit_json(changed=changed, ansible_facts=ansible_facts)


from ansible.module_utils.basic import AnsibleModule
main()
