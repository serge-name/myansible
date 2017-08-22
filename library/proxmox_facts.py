#!/usr/bin/python

PROXMOX_PKG_NAME = 'proxmox-ve'

from ansible.module_utils import dpkg

def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
        supports_check_mode = True
    )

    facts = {}

    if dpkg.get_pkg_status(PROXMOX_PKG_NAME):
        version = dpkg.get_pkg_version(PROXMOX_PKG_NAME)
        facts['pve_major_version'] = version.split('.')[0]
        facts['pve_version'] = version

    module.exit_json(changed=False, ansible_facts={'proxmox_facts': facts})

from ansible.module_utils.basic import AnsibleModule
main()
