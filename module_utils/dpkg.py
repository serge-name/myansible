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
