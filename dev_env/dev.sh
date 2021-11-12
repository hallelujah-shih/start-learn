# golang
mkdir -p $HOME/go/bin
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

source /opt/goenv

# kernel dev
export KDIR=/lib/modules/$(uname -r)/build
export ARCH=$(echo $(arch) | sed 's/x86_64/x86/g')

