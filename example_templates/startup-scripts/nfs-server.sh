#!/bin/bash

set -x

# Install requirements
apt-get update 
apt-get install -y --no-install-recommends \
  netbase \
  nfs-kernel-server

# Setup exports
EXPORTS_BASE="/exports/"
mkdir -p /exports
mount /dev/disk/by-id/google-nfs-server /exports/
for d in `find ${EXPORTS_BASE} -maxdepth 1 -type d`; do
  if [ "${d}" == "${EXPORTS_BASE}" ]; then
    continue
  fi
  echo "Adding ${d} to /etc/exports..."
  echo "${d} *(rw,sync,insecure,fsid=0,no_subtree_check,no_root_squash)" >> /etc/exports
done

service nfs-kernel-server restart
