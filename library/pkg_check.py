#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# - name: check whether tcpdump has been installed
#   pkg_check:
#     name: tcpdump
#   register: tcpdump_status
#
# - name: check tcpdump version
#   pkg_check:
#     name: tcpdump
#     op: ge
#     version: 1.2.3
#   register: tcpdump_status

# FIXME: use https://github.com/theclimatecorporation/python-dpkg

from ansible.module_utils import dpkg

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name        = dict(type='str', required=True),
            op          = dict(type='str', required=False),
            version     = dict(type='str', required=False),
        ),
        supports_check_mode = True
    )

    name = module.params['name']

    installed = dpkg.get_pkg_status(name)

    op = module.params['op']
    reference_version = module.params['version']
    if bool(op) ^ bool(reference_version):
        module.exit_json(msg="use both op= and version=", failed=True)

    actual_version = dpkg.get_pkg_version(name)

    args = { 'msg': 'OK', 'changed': False }

    if not bool(op):
        args['installed'] = installed
        args['version'] = actual_version
    elif installed == False:
        args['installed'] = False
        args['version'] = ""
        args['result'] = False
    else:
        args['installed'] = True
        args['version'] = actual_version
        args['result'] = dpkg.do_compare_versions(actual_version, op, reference_version)

    module.exit_json(**args)

# import module snippets
from ansible.module_utils.basic import *
main()
