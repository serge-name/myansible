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
    def write_to_file(path, string):
        f = open(path, 'w')
        f.write(string)
        f.close()

    module = AnsibleModule(
        argument_spec = dict(
            phase = dict(default='single', choices=['single','pre','post']),
        ),
        supports_check_mode = True
    )

    args = {}
    fact_path = os.path.join(ASNIBLE_FACTS_PATH, "{}.fact".format(FACT_NAME))

    changed = False if module.check_mode else mkdir_p(ASNIBLE_FACTS_PATH)

    if not os.path.isfile(fact_path):
        if module.params['phase'] != 'pre':
            if not module.check_mode:
                write_to_file(fact_path, "false\n")
            changed = True
        args['ansible_facts'] = { 'ansible_local': { FACT_NAME: True } }

    args['changed'] = changed

    module.exit_json(**args)


from ansible.module_utils.basic import AnsibleModule
main()
