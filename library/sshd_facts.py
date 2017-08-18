#!/usr/bin/python

SSHD_DEFAULT_PATH = '/usr/sbin/sshd'

import commands

def chk_ed25519(path):
    rc, _ = commands.getstatusoutput("grep -qs 'ed25519' {}".format(path))

    rc >>= 8

    if rc == 0:
        return True
    elif rc == 1:
        return False
    else:
        return None


def main():
    module = AnsibleModule(
        argument_spec = dict(
            path = dict(type='str', required=False, default=SSHD_DEFAULT_PATH),
        ),
        supports_check_mode = True
    )

    path = module.params['path']

    facts = {
      'ed25519_supported': chk_ed25519(path)
    }

    module.exit_json(changed=False, ansible_facts={'sshd_facts': facts})

from ansible.module_utils.basic import *
main()
