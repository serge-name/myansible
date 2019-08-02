from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def get_interfaces(self, variables):
        try:
            return variables['tinc__nets'].keys()
        except KeyError:
            return []

    def get_interface_data(self, v, iface):
        ret = {}
        complete = True
        if 'tinc__nets' in v and iface in v['tinc__nets']:
            ret = v['tinc__nets'][iface]
            for fact in ['host_name', 'pub_key']:
                try:
                    ret[fact] = v['tinc_facts']['nets'][iface][fact]
                except KeyError:
                    complete = False
            if 'routes' not in ret:
                ret['routes'] = []
            ret['ansible_default_ipv4_address'] = v['ansible_default_ipv4']['address']
            ret['ansible_default_ipv6_address'] = v['ansible_default_ipv6'].get('address', '')

        return complete, ret

    def record_interface_data(self, ret, r, h, i):
        if r:
            if i not in ret:
                ret[i] = {}
            ret[i][h] = r

    def run(self, terms, variables, **kwargs):
        hostvars = variables['hostvars']

        ret = {}
        ifaces = self.get_interfaces(variables)
        complete = True

        for i in ifaces:
            for h, v in hostvars.items():
                c, r = self.get_interface_data(v, i)
                self.record_interface_data(ret, r, h, i)
                if not c:
                    complete = False

        return [{'complete':complete,'data':ret}]
