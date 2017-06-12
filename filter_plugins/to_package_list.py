class FilterModule(object):
    ''' A Comment '''

    def filters(self):
        return {
            'to_package_list': self.to_package_list,
        }

    def to_package_list(self,input_value):
        packages = []
        for pkg, ver in input_value.items():
            if ver == True:
                packages.append(pkg)
            elif ver == False:
                None
            else:
                packages.append('{}={}'.format(pkg, ver))

        return ",".join(packages)
