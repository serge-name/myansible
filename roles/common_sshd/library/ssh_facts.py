#!/usr/bin/env python3

from subprocess import run, PIPE
from re import match

try:
    from functools import cached_property
except ImportError:
    # use own implementation if python<3.8
    def cached_property(func):
        def inner(self):
            if func.__name__ not in self.__dict__:
                res = func(self)
                self.__dict__[func.__name__] = res
            return self.__dict__[func.__name__]
        return property(inner)


SSH_ALGO_CONSTRAINTS = {
    'cipher': {
        'bad': (
            '3des-cbc', 'aes128-cbc', 'aes192-cbc', 'aes256-cbc', 'rijndael-cbc@lysator.liu.se',
            'arcfour256', 'arcfour128', 'arcfour', 'cast128-cbc', 'blowfish-cbc',
        ),
        'preference': ('chacha20-poly1305@openssh.com', 'aes256-gcm@openssh.com', 'aes128-gcm@openssh.com', ),
    },
    'kex': {
        # https://tools.ietf.org/id/draft-ietf-curdle-ssh-kex-sha2-11.html
        # https://tools.ietf.org/id/draft-ietf-curdle-ssh-kex-sha2-13.html
        'bad': (
            'diffie-hellman-group1-sha1', 'diffie-hellman-group14-sha1', 'diffie-hellman-group-exchange-sha1',
            'ecdh-sha2-nistp256', 'ecdh-sha2-nistp384', 'ecdh-sha2-nistp521',
        ),
        'preference': (
            'sntrup4591761x25519-sha512@tinyssh.org', 'curve25519-sha256@libssh.org', 'curve25519-sha256',
            'diffie-hellman-group16-sha512', 'diffie-hellman-group18-sha512',
        ),
    },
    'mac': {
        'bad': (
            'hmac-sha1', 'hmac-sha1-96', 'hmac-sha1-etm@openssh.com', 'hmac-sha1-96-etm@openssh.com',
            'hmac-md5', 'hmac-md5-96', 'hmac-md5-etm@openssh.com', 'hmac-md5-96-etm@openssh.com',
            'umac-64@openssh.com', 'umac-64-etm@openssh.com',
            'hmac-ripemd160-etm@openssh.com', 'hmac-ripemd160@openssh.com', 'hmac-ripemd160',
            'umac-128-etm@openssh.com', 'umac-128@openssh.com',
        ),
        'preference': ('hmac-sha2-512-etm@openssh.com', 'hmac-sha2-256-etm@openssh.com', 'hmac-sha2-512', 'hmac-sha2-256', ),
    },
    'key': {
        'bad': (
            'ssh-dss', 'ssh-dss-cert-v01@openssh.com',
            'ecdsa-sha2-nistp521-cert-v01@openssh.com', 'ecdsa-sha2-nistp384-cert-v01@openssh.com', 'ecdsa-sha2-nistp256-cert-v01@openssh.com',
            'ecdsa-sha2-nistp521', 'ecdsa-sha2-nistp384', 'ecdsa-sha2-nistp256',
        ),
        'preference': ('sk-ssh-ed25519-cert-v01@openssh.com', 'sk-ssh-ed25519@openssh.com', 'ssh-ed25519-cert-v01@openssh.com', 'ssh-ed25519', ),
    },
}


class SSH:
    def __init__(self):
        self.algos_dict = {}

    @cached_property
    def version(self):
        version_string = run(['ssh', '-V'], stderr=PIPE).stderr.decode('utf-8').strip()
        result = {
            'full_string': version_string,
            'detected': False,
        }
        r_match = match(r'^OpenSSH_(\d+)\.(\d+)p(\d+)\s+.*OpenSSL\s+(\S+)\s+', version_string)
        if r_match:
            result.update({
                'detected': True,
                'major': r_match.group(1),
                'minor': r_match.group(2),
                'patchlevel': r_match.group(3),
                'openssl': r_match.group(4),
            })
        return result

    def algos(self, query):
        if query in self.algos_dict:
            return self.algos_dict[query]

        constraints = SSH_ALGO_CONSTRAINTS.get(query, {
            'bad': tuple(),
            'preference': tuple(),
        })
        available = run(['ssh', '-Q', query], stdout=PIPE).stdout.decode('utf-8').splitlines()
        available.reverse()

        rest = available.copy()
        result = []
        for el in constraints['preference']:
            if el in rest:
                result.append(el)
                rest.remove(el)
        for el in constraints['bad']:
            if el in rest:
                rest.remove(el)
        result.extend(rest)
        return {
            'available': available,
            'selected': result,
        }


def main():
    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode = True,
    )
    ssh = SSH()

    facts = {
        'version': ssh.version,
    }
    facts.update({
        el: ssh.algos(el) for el in ('cipher', 'kex', 'mac', 'key', )
    })

    module.exit_json(changed=False, ansible_facts={'ssh_facts': facts})


from ansible.module_utils.basic import AnsibleModule
main()
