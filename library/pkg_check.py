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

import commands

def get_pkg_status(package):
    _, status = commands.getstatusoutput("dpkg-query  --show --showformat='${{Status}}' '{}' 2>/dev/null".format(package))

    return (status == 'install ok installed')

def get_pkg_version(package):
    _, version = commands.getstatusoutput("dpkg-query  --show --showformat='${{Version}}' '{}' 2>/dev/null".format(package))

    return version

def do_compare_versions(ver1, op, ver2):
    status, _ = commands.getstatusoutput("dpkg --compare-versions '{}' {} '{}'".format(ver1, op, ver2))

    return not bool(status)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name        = dict(type='str', required=True),
            op          = dict(type='str', required=False),
            version     = dict(type='str', required=False),
        )
    )

    name = module.params['name']

    installed = get_pkg_status(name)

    op = module.params['op']
    reference_version = module.params['version']
    if bool(op) ^ bool(reference_version):
        module.exit_json(msg="use both op= and version=", failed=True)

    actual_version = get_pkg_version(name)

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
        args['result'] = do_compare_versions(actual_version, op, reference_version)

    module.exit_json(**args)

# import module snippets
from ansible.module_utils.basic import *
main()
