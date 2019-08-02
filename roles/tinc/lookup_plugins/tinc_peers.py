from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def get_defined(self, hostvars, iface):
        try:
            ret = hostvars['tinc__nets'][iface]
        except KeyError:
            ret = {}

        return ret

    def get_collected(self, facts, iface):
        try:
            ret = facts['tinc_facts']['nets'][iface]
        except KeyError:
            ret = {}

        return ret

    def get_interface_data(self, hostvars, iface):
        hostfacts = hostvars['ansible_facts']
        complete = True
        ret = {
            **self.get_defined(hostvars, iface),
            **self.get_collected(hostfacts, iface),
        }

        if ret:
            for fact in ['host_name', 'pub_key', 'address']:
                if fact not in ret:
                    complete = False

            if 'routes' not in ret:
                ret['routes'] = []

            ret['default_ipv4_address'] = hostfacts.get('default_ipv4', {}).get('address', '')
            ret['default_ipv6_address'] = hostfacts.get('default_ipv6', {}).get('address', '')

        return complete, ret

    def run(self, terms, variables, **kwargs):
        ret = {}
        complete = True

        for iface in variables.get('tinc__nets', {}).keys():
            for host in variables['hostvars'].keys():
                c, r = self.get_interface_data(variables['hostvars'][host], iface)

                if r:
                    if iface not in ret:
                        ret[iface] = {}
                    ret[iface][host] = r

                if not c:
                    complete = False

        return [{'complete':complete,'data':ret}]
