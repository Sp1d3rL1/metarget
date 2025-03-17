import platform


# default CNI plugin
DEFAULT_CNI_PLUGIN = 'flannel'
# default kata runtime type
DEFAULT_KATA_RUNTIME_TYPE = 'qemu'

# currently supported gadgets
gadgets_supported = [
    'docker',
    'k8s',
    'kata',
    'kernel',
    'containerd',
    'runc',
]

docker_default_version = '20.10.24'
k8s_default_version = '1.28.4'
kata_default_version = '3.0.0'
kernel_default_version = '5.14.0-362.el9.x86_64'
containerd_default_version = '1.7.3'
runc_default_version = '1.1.7'

# Kubernetes DNF/Yum Repository
k8s_dnf_repo_gpg = "https://packages.cloud.google.com/yum/doc/yum-key.gpg"
k8s_dnf_repo_entry = "https://pkgs.k8s.io/core:/stable:/v1.28/rpm/"

# Docker DNF/Yum Repository
docker_dnf_repo_gpg = "https://download.docker.com/linux/rhel/gpg"
docker_dnf_repo_entry = "https://download.docker.com/linux/rhel/docker-ce.repo"

# Kubernetes image sources
k8s_images_prefix_official = "registry.k8s.io/"
k8s_images_prefix_candidate = k8s_images_prefix_official

# Quay images source
quay_images_prefix_official = "quay.io/"
quay_images_prefix_candidate = quay_images_prefix_official

# Docker images source
docker_images_prefix_official = "docker.io/"
docker_image_prefix_candidate = docker_images_prefix_official

# Active Kubernetes repository
k8s_repo_gpg = k8s_dnf_repo_gpg
k8s_repo_entry = k8s_dnf_repo_entry

# Active Docker repository
docker_repo_gpg = docker_dnf_repo_gpg
docker_repo_entry = docker_dnf_repo_entry

# Available CNI plugins
available_cni_plugins = [
    'flannel',
    'calico',
    'cilium',
]
cni_plugin_cidrs = {
    'flannel': '10.244.0.0/16',
    'calico': '10.10.0.0/16',
    'cilium': '10.10.0.0/16',
}

# Available kubectl versions for dnf
dnf_kubectl_versions = [
    "1.23.17-0", "1.23.16-0", "1.23.15-0", "1.23.14-0", "1.23.13-0", "1.23.12-0", "1.23.11-0", "1.23.10-0",
    "1.23.9-0", "1.23.8-0", "1.23.7-0", "1.23.6-0", "1.23.5-0", "1.23.4-0", "1.23.3-0", "1.23.2-0", "1.23.1-0",
    "1.23.0-0", "1.22.17-0", "1.22.16-0", "1.22.15-0", "1.22.14-0", "1.22.13-0", "1.22.12-0", "1.22.11-0",
    "1.22.10-0", "1.22.9-0", "1.22.8-0", "1.22.7-0", "1.22.6-0", "1.22.5-0", "1.22.4-0", "1.22.3-0",
    "1.22.2-0", "1.22.1-0", "1.22.0-0", "1.21.14-0", "1.21.13-0", "1.21.12-0", "1.21.11-0", "1.21.10-0",
    "1.21.9-0", "1.21.8-0", "1.21.7-0", "1.21.6-0", "1.21.5-0", "1.21.4-0", "1.21.3-0", "1.21.2-0",
    "1.21.1-0", "1.21.0-0", "1.20.15-0", "1.20.14-0", "1.20.13-0", "1.20.12-0", "1.20.11-0", "1.20.10-0",
    "1.20.9-0", "1.20.8-0", "1.20.7-0", "1.20.6-0", "1.20.5-0", "1.20.4-0", "1.20.2-0", "1.20.1-0",
    "1.20.0-0", "1.19.16-0", "1.19.15-0", "1.19.14-0", "1.19.13-0", "1.19.12-0", "1.19.11-0", "1.19.10-0",
    "1.19.9-0", "1.19.8-0", "1.19.7-0", "1.19.6-0", "1.19.5-0", "1.19.4-0", "1.19.3-0", "1.19.2-0",
    "1.19.1-0", "1.19.0-0"
]