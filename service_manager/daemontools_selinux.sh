#!/bin/bash

dnf -y install policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted libselinux-utils setroubleshoot-server setools setools-console mcstrans


grep -a scanboot /var/log/audit/audit.log | audit2allow -M daemontools
semodule -i daemontools.pp
rm daemontools.pp -f
