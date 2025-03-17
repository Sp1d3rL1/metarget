import copy
import subprocess
import docker
import socket
import requests
from tqdm import tqdm

import config
import utils.system as system_func
import utils.verbose as verbose_func
import utils.color_print as color_print


class Installer(object):
    cmd_dnf_uninstall = "dnf -y remove".split()
    cmd_dnf_update = "dnf check-update".split()
    cmd_dnf_install = "dnf -y install".split()
    cmd_dnf_repoquery = "dnf repoquery".split()
    cmd_rpm_search = "rpm -qa".split()
    try:
        docker_client = docker.from_env()
    except BaseException:
        pass

    @classmethod
    def _get_dnf_complete_version(cls, name, version, verbose=False):
        _, stderr = verbose_func.verbose_output(verbose)
        temp_cmd = copy.copy(cls.cmd_dnf_repoquery)
        temp_cmd.extend(["--show-duplicates", name])
        try:
            res = subprocess.run(
                temp_cmd,
                stdout=subprocess.PIPE,
                stderr=stderr,
                check=True)
        except subprocess.CalledProcessError:
            return None
        entries = res.stdout.decode('utf-8').split('\n')
        complete_version = None
        version_candidates = [entry.strip() for entry in entries if version in entry]
        if version_candidates:
            complete_version = version_candidates[-1]
        return complete_version

    @classmethod
    def _install_one_gadget_by_version(
            cls, name, version, mappings=None, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        complete_version = cls._get_dnf_complete_version(
            name, version, verbose=verbose)
        if complete_version:
            color_print.debug(
                'Installing {gadget} with {version} version'.format(
                    gadget=name, version=complete_version))
            temp_cmd = copy.copy(cls.cmd_dnf_install)
            temp_cmd.append(
                '{name}-{version}'.format(
                    name=name,
                    version=complete_version))
            try:
                subprocess.run(
                    temp_cmd,
                    stderr=stderr,
                    stdout=stdout,
                    check=True)
            except subprocess.CalledProcessError:
                return False
            if mappings:
                mappings[name] = complete_version
            return True
        color_print.warning('No candidate version for %s' % name)
        return False

    @classmethod
    def _dnf_update(cls, verbose=False):
        stdout, stderr = verbose_func.verbose_output(verbose)
        try:
            subprocess.run(
                cls.cmd_dnf_update,
                stdout=stdout,
                stderr=stderr,
                check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def reload_and_restart_docker(verbose=False):
        if not system_func.reload_daemon_config(verbose=verbose):
            return False
        stdout, stderr = verbose_func.verbose_output(verbose)
        color_print.debug('Restarting Docker')
        try:
            subprocess.run(
                'systemctl restart docker'.split(),
                stdout=stdout,
                stderr=stderr,
                check=True)
            return True
        except subprocess.CalledProcessError:
            color_print.error('Failed to restart Docker')
            return False
