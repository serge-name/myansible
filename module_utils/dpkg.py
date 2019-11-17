import subprocess
import os

def run_command(*args):
    rc = 0

    try:
        output = subprocess.check_output(args, stderr=open(os.devnull, 'w')).decode()
    except subprocess.CalledProcessError as e:
        output = e.output
        rc = e.returncode

    return rc, output

def get_pkg_status(package):
    _, pkg_status = run_command('dpkg-query', '--show', '--showformat=${Status}', package)

    return (pkg_status == 'install ok installed')

def get_pkg_version(package):
    _, version = run_command('dpkg-query', '--show', '--showformat=${Version}', package)

    return version

def do_compare_versions(ver1, op, ver2):
    rc, _ = run_command('dpkg', '--compare-versions', ver1, op, ver2)

    return not bool(rc)
