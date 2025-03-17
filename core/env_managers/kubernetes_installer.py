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

docker_default_version = '20.10.14'
k8s_default_version = '1.22.2'
kata_default_version = '2.0.0'
kernel_default_version = '4.18.0-305.el8.x86_64'
containerd_default_version = '1.2.6'
runc_default_version = '1.0.0-rc8'

# Kubernetes Yum Repository
k8s_yum_repo_gpg = "https://packages.cloud.google.com/yum/doc/yum-key.gpg"
k8s_yum_repo_entry = "https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64"

# Docker Yum Repository
docker_yum_repo_gpg = "https://download.docker.com/linux/centos/gpg"
docker_yum_repo_entry = "https://download.docker.com/linux/centos/docker-ce.repo"

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
k8s_repo_gpg = k8s_yum_repo_gpg
k8s_repo_entry = k8s_yum_repo_entry

# Active Docker repository
docker_repo_gpg = docker_yum_repo_gpg
docker_repo_entry = docker_yum_repo_entry

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
