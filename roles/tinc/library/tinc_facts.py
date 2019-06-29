#!/usr/bin/python

TINC_CONF_BASE = '/etc/tinc'
TINC_DEFAULT_CONF_NAME = 'default'

import os
import subprocess
import re


def get_node_variable(conf_path, var):
    try:
        res = subprocess.check_output(
            ['tinc', '--config={}'.format(conf_path), 'get', var]
        ).splitlines()
    except subprocess.CalledProcessError:
        res = []

    return res


def get_net_info(conf_path):
    info = {}

    host_name = get_node_variable(conf_path, "Name")
    pub_key = get_node_variable(conf_path, "Ed25519PublicKey")

    if host_name and pub_key:
        info['host_name'] = host_name[0]
        info['pub_key'] = pub_key[0]

    return info


def main():
    module = AnsibleModule(
        argument_spec = dict(
            conf_base = dict(type='str',  required=False, default=TINC_CONF_BASE),
        ),
        supports_check_mode = True
    )

    conf_base = module.params['conf_base']
    facts = { 'nets': {} }

    def add_unless_empty(d, key, value):
        if value:
            d[key] = value

    try:
        add_unless_empty(facts['nets'], TINC_DEFAULT_CONF_NAME, get_net_info(conf_base))
        for net in os.listdir(conf_base):
            conf_path = os.path.join(conf_base, net)
            add_unless_empty(facts['nets'], net, get_net_info(conf_path))

    except OSError:
        pass

    module.exit_json(changed=False, ansible_facts={'tinc_facts': facts})


from ansible.module_utils.basic import AnsibleModule
main()
