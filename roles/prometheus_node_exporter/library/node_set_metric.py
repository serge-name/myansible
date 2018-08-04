#!/usr/bin/python
# coding: utf-8

TEXTFILE_DIR = '/var/lib/prometheus/node-exporter'
DEFAULT_HELP_TEXT = 'A metric'

# - node_set_metric:
#     name:      "location_dc"
#     content:   "msk"
#     help_test: "a metric"
#     state:     present
#   become_user: prometheus

# - node_set_metric:
#     name:      "obsolete"
#     state:     absent
#   become_user: prometheus

import os
import filecmp
from tempfile import mkstemp


def metric_file_path(name):
    return os.path.join(TEXTFILE_DIR, "{}.prom".format(name))


def metric_remove(name):
    textfile = metric_file_path(name)

    try:
        if os.path.isfile(textfile):
            os.remove(textfile)
            return {"msg":"OK", "failed":False, "changed":True}
    except OSError as e:
        return {"msg":e, "failed":True, "changed":False}

    return {"msg":"OK", "failed":False, "changed":False}


def metric_set(name, content, help_text):
    full_name = "node_{}".format(name)
    textfile = metric_file_path(name)

    try:
        fd, tmp_path = mkstemp(prefix=name, dir=TEXTFILE_DIR)
        os.write(fd, "# HELP {} {}\n".format(full_name, help_text))
        os.write(fd, "# TYPE {} untyped\n".format(full_name))
        os.write(fd, "{}{}{}=\"{}\"{} 1\n".format(full_name, '{', full_name, content, "}"))
        os.close(fd)
    except OSError as e:
        if os.path.isfile(tmp_path):
            os.remove(tmp_path)
        return {"msg":e, "failed":True, "changed":False}

    if os.path.isfile(textfile):
        if filecmp.cmp(tmp_path, textfile, False):
            os.remove(tmp_path)
            return {"msg":"OK", "failed":False, "changed":False}

        try:
            os.remove(textfile)
        except OSError as e:
            return {"msg":e, "failed":True, "changed":False}

    try:
        os.rename(tmp_path, textfile)
    except OSError as e:
        return {"msg":e, "failed":True, "changed":True}

    os.chmod(textfile, 0644)

    return {"msg":"OK", "failed":False, "changed":True}


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name      = dict(type='str', required=True),
            content   = dict(type='str', required=False, default=None),
            help_text = dict(type='str', required=False, default=DEFAULT_HELP_TEXT),
            state  = dict(choices=['present','absent'], required=False, default='present'),
        )
    )

    name      = module.params['name']
    content   = module.params['content']
    help_text = module.params['help_text']
    state     = module.params['state']

    if state == 'absent':
        module.exit_json(**metric_remove(name))

    if state == 'present' and content is None:
        module.exit_json(msg="content must be defined", failed=True)

    module.exit_json(**metric_set(name, content, help_text))


from ansible.module_utils.basic import *
main()
