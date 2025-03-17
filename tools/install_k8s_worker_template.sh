#!/bin/bash

# run as root
# currently docker should be installed

# clear potential old components
if kubeadm reset --help | grep force &> /dev/null; then
  kubeadm reset --force
else
  kubeadm reset
fi

dnf -y remove kubeadm kubelet

# pre_configure
modprobe br_netfilter
echo "net.bridge.bridge-nf-call-ip6tables = 1" > /etc/sysctl.d/k8s.conf
echo "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.d/k8s.conf
swapoff -a
sed -i '/\/swapfile/s/^/#/' /etc/fstab
sed -i '/\/swap.img/s/^/#/' /etc/fstab

# pre_install
dnf -y install curl

dnf config-manager --add-repo ${repo_entry}
rpm --import ${gpg_url}
dnf -y install kubelet-${kubelet_version} kubeadm-${kubeadm_version} kubernetes-cni-${kubernetes_cni_version}

# enable and start kubelet
systemctl enable --now kubelet

# pull images
${cmds_pull_images}

# join cluster
kubeadm join ${master_ip}:6443 --token ${token} \
    --discovery-token-ca-cert-hash sha256:${ca_cert_hash} ${kubeadm_options}