#!/usr/bin/python

PROXMOX_PKG_NAME = 'proxmox-ve'

import commands

def get_pkg_status(package):
    _, status = commands.getstatusoutput("dpkg-query  --show --showformat='${{Status}}' '{}' 2>/dev/null".format(package))

    return (status == 'install ok installed')


def get_pkg_version(package):
    _, version = commands.getstatusoutput("dpkg-query  --show --showformat='${{Version}}' '{}' 2>/dev/null".format(package))

    return version


def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
        supports_check_mode = True
    )

    facts = {}

    if get_pkg_status(PROXMOX_PKG_NAME):
        version = get_pkg_version(PROXMOX_PKG_NAME)
        facts['pve_major_version'] = version.split('.')[0]
        facts['pve_version'] = version

    module.exit_json(changed=False, ansible_facts={'proxmox_facts': facts})

from ansible.module_utils.basic import AnsibleModule
main()
