#!/usr/bin/python
# coding: utf-8

def main():
    module = AnsibleModule(
        argument_spec = dict(
            msg         = dict(type='str',  required=False, default=""),
            changed     = dict(type='bool', required=False, default=False),
            failed      = dict(type='bool', required=False, default=False),
        ),
        supports_check_mode = True
    )

    msg = module.params['msg']
    changed = module.params['changed']
    failed = module.params['failed']

    module.exit_json(msg=msg, changed=changed, failed=failed)

from ansible.module_utils.basic import *
main()
