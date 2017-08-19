#!/usr/bin/python
# coding: utf-8

#
# - name: get pw database record by user name
#   getpw:
#     user: root
#   register: foo
#
# - name: get pw database record by user id
#   getpw:
#     user: 0
#   register: bar
#

import pwd


def getpw(user):
    try:
        uid = int(user)
    except ValueError:
        uid = None

    try:
        if uid is not None:
            pw = pwd.getpwuid(uid)
        else:
            pw = pwd.getpwnam(user)
    except KeyError:
        pw = None

    return pw


def pw2dict(pw):
    if pw is None:
        result = {}
    else:
        result = {
          'name':   pw.pw_name,
          'passwd': pw.pw_passwd,
          'uid':    pw.pw_uid,
          'gid':    pw.pw_gid,
          'gecos':  pw.pw_gecos,
          'dir':    pw.pw_dir,
          'shell':  pw.pw_shell,
        }

    return result


def main():
    module = AnsibleModule(
        argument_spec = dict(
            user        = dict(type='str', required=True),
            ignore      = dict(type='bool', required=False, default=False),
        ),
        supports_check_mode = True
    )

    user = module.params['user']
    ignore = module.params['ignore']

    pw = getpw(user)

    args = {
        'changed': False,
        'pw': pw2dict(pw),
    }

    if pw is None:
        args['msg'] = "user/uid {} not found".format(user)
        args['exists'] = False
        args['failed'] = (not ignore)
    else:
        args['msg'] = "OK"
        args['exists'] = True

    module.exit_json(**args)

from ansible.module_utils.basic import AnsibleModule
main()
