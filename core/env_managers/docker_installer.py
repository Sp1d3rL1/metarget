import copy
import subprocess
import os
import utils.color_print as color_print
import utils.verbose as verbose_func
import config
import utils.checkers as checkers
from core.env_managers.installer import Installer


class DockerInstaller(Installer):
    _docker_gadgets = [
        'docker-ce',
        'docker-ce-cli',
        'docker',
        'containerd.io',
        'runc',
    ]
    _docker_requirements = [
        'yum-utils',
        'device-mapper-persistent-data',
        'lvm2',
    ]

    @classmethod
    def uninstall(cls, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        for gadget in cls._docker_gadgets:
            temp_cmd = ["dnf", "remove", "-y", gadget]
            subprocess.run(
                temp_cmd,
                stdout=stdout,
                stderr=stderr,
                check=False
            )

    @classmethod
    def uninstall_containerd_only(cls, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        temp_cmd = ["dnf", "remove", "-y", "containerd.io"]
        subprocess.run(
            temp_cmd,
            stdout=stdout,
            stderr=stderr,
            check=False
        )

    @classmethod
    def uninstall_runc(cls, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        color_print.debug('Uninstalling runc')
        subprocess.run(["rm", "-f", "/usr/bin/runc"], stdout=stdout, stderr=stderr, check=True)

    @classmethod
    def install_by_version(cls, gadgets, context=None, verbose=False):
        if not cls._pre_install(verbose=verbose):
            color_print.error('Failed to install prerequisites')
            return False
        for gadget in gadgets:
            if not cls._install_one_gadget_by_version(
                    gadget['name'], gadget['version'], verbose=verbose):
                color_print.error('Some errors happened during Docker installation')
                return True
        return True

    @classmethod
    def _pre_install(cls, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        color_print.debug('Installing prerequisites')
        try:
            subprocess.run(["dnf", "install", "-y"] + cls._docker_requirements, stdout=stdout, stderr=stderr, check=True)
            subprocess.run(["dnf", "config-manager", "--add-repo", "https://download.docker.com/linux/centos/docker-ce.repo"],
                           stdout=stdout, stderr=stderr, check=True)
        except subprocess.CalledProcessError:
            return False
        return True

    @classmethod
    def install_runc(cls, install_version, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        color_print.debug(f'Installing runc with version {install_version}')

        proxy_urls = [
            'https://github.moeyy.xyz',
            'https://gh-proxy.com',
            'https://ghproxy.net'
        ]

        url = f'https://github.com/opencontainers/runc/releases/download/v{install_version}/runc.amd64'

        for proxy_url in proxy_urls:
            download_url = f'{proxy_url}/{url}'
            try:
                runc_commands = [
                    'mv /usr/bin/runc /usr/bin/runc.bak',
                    f'curl -L -o /usr/bin/runc {download_url}',
                    'chmod +x /usr/bin/runc',
                    'systemctl daemon-reload',
                    'systemctl restart docker'
                ]
                color_print.warning(f'Attempting to download runc from {download_url}')
                for command in runc_commands:
                    subprocess.run(command.split(), stdout=stdout, stderr=stderr, check=True)
                return True
            except subprocess.CalledProcessError:
                color_print.error(f'Failed to download runc from {download_url}. Trying next proxy...')
                continue

        color_print.error('All download attempts failed. Restoring the original runc.')
        try:
            subprocess.run(['mv', '/usr/bin/runc.bak', '/usr/bin/runc'], stdout=stdout, stderr=stderr, check=True)
            checkers.runc_executable(verbose=verbose)
        except subprocess.CalledProcessError:
            color_print.error('Failed to restore original runc.')
        return False


if __name__ == "__main__":
    DockerInstaller.uninstall()
    import sys
    if len(sys.argv) > 1:
        test_version = sys.argv[1]
    else:
        test_version = '17.03.0'
    temp_gadgets = [{'name': 'docker-ce', 'version': test_version}]
    DockerInstaller.install_by_version(temp_gadgets)
