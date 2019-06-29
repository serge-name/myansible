#!/usr/bin/python

SSHD_DEFAULT_PATH = '/usr/sbin/sshd'

import subprocess

def chk_ed25519(path):
    try:
        rc = subprocess.check_call(['grep', '-qs', 'ed25519', path])
    except subprocess.CalledProcessError as e:
        rc = e.returncode

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
