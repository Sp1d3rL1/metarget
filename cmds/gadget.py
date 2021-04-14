"""
Gadget Commands
"""

import config
import utils.color_print as color_print
import utils.checkers as checkers
import utils.system as system_func
from core.env_managers.docker_installer import DockerInstaller
from core.env_managers.kubernetes_installer import KubernetesInstaller
from core.env_managers.kernel_installer import KernelInstaller
from core.env_managers.kata_containers_installer import KataContainersInstaller


def install(args):
    """Install a cloud native gadget with specified version.

    Args:
        args.gadget: Name of the specified cloud native gadget.
        args.verbose: Verbose or not.
      Args below only used when installing Kubernetes:
        args.cni: Name of CNI plugin.
        args.pod_network_cidr: CIDR of pod network.
        args.domestic: Pull Kubernetes images from domestic source or not.
        args.taint_master: Taint the master node or not.
        args.http_proxy: HTTP proxy used when pulling official images.
        args.no_proxy: Domains which should be visited without proxy.

    Returns:
        None.
    """
    if args.gadget == 'docker':
        temp_gadgets = [{'name': 'docker-ce', 'version': args.version}]
        if checkers.docker_specified_installed(temp_gadgets):
            color_print.debug(
                '{gadget} with version {version} already installed'.format(
                    gadget=args.gadget, version=args.version))
            return
        color_print.debug('uninstall current docker if applicable')
        DockerInstaller.uninstall(verbose=args.verbose)
        if not DockerInstaller.install_by_version(
                temp_gadgets, verbose=args.verbose):
            color_print.error(
                'error: failed to install {gadget}'.format(
                    gadget=args.gadget))
        else:
            color_print.debug(
                '{gadget} with version {version} successfully installed'.format(
                    gadget=args.gadget, version=args.version))
    if args.gadget == 'k8s':
        temp_gadgets = [
            {'name': 'kubelet', 'version': args.version},
            {'name': 'kubeadm', 'version': args.version},
            {'name': 'kubectl', 'version': args.version},
        ]
        if checkers.kubernetes_specified_installed(
                temp_gadgets, verbose=args.verbose):
            color_print.debug(
                '{gadget} with version {version} already installed'.format(
                    gadget=args.gadget, version=args.version))
            return
        color_print.debug('uninstall current kubernetes if applicable')
        KubernetesInstaller.uninstall(verbose=args.verbose)
        temp_pod_network_cidr = args.pod_network_cidr if args.pod_network_cidr else config.cni_plugin_cidrs[
            args.cni]
        if not KubernetesInstaller.install_by_version(temp_gadgets,
                                                      cni_plugin=args.cni,
                                                      pod_network_cidr=temp_pod_network_cidr,
                                                      domestic=args.domestic,
                                                      taint_master=args.taint_master,
                                                      http_proxy=args.http_proxy,
                                                      no_proxy=args.no_proxy,
                                                      verbose=args.verbose):
            color_print.error(
                'error: failed to install {gadget}'.format(
                    gadget=args.gadget))
        else:
            color_print.debug(
                '{gadget} successfully installed'.format(
                    gadget=args.gadget))
    if args.gadget == 'kernel':
        temp_gadgets = [
            {'name': 'kernel', 'version': args.version},
        ]
        if checkers.kernel_specified_installed(
                temp_gadgets, verbose=args.verbose):
            color_print.debug(
                '{gadget} with version {version} already installed'.format(
                    gadget=args.gadget, version=args.version))
            return
        if not KernelInstaller.install_by_version(
                temp_gadgets, verbose=args.verbose):
            color_print.error(
                'error: failed to install {gadget}'.format(
                    gadget=args.gadget))
        else:
            color_print.debug(
                '{gadget} successfully installed'.format(
                    gadget=args.gadget))
            # reboot
            reboot = color_print.debug_input('reboot system now? (y/n) ')
            if reboot == 'y' or reboot == 'Y':
                system_func.reboot_system(verbose=args.verbose)


def remove(args):
    """Remove an installed cloud native gadget.

    Args:
        args.gadget: Name of the specified cloud native gadget.
        args.verbose: Verbose or not.

    Returns:
        None.
    """
    if args.gadget == 'docker':
        DockerInstaller.uninstall(verbose=args.verbose)
        color_print.debug(
            '{gadget} successfully removed'.format(
                gadget=args.gadget))
    if args.gadget == 'k8s':
        KubernetesInstaller.uninstall(verbose=args.verbose)
        color_print.debug(
            '{gadget} successfully removed'.format(
                gadget=args.gadget))
    if args.gadget == 'kernel':
        color_print.warning(
            'removal of {gadget} is unsupported'.format(
                gadget=args.gadget))


def retrieve(args):
    print(config.gadgets_supported)
