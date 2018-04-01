# devtoolset
```
Developer Toolset is designed for developers working on CentOS or Red Hat Enterprise Linux platform. It provides current versions of the GNU Compiler Collection, GNU Debugger, Eclipse development platform, and other development, debugging, and performance monitoring tools.
```

## 安装
```
1. 为你的系统安装仓库
   * CentOS
       # sudo yum install centos-release-sc1
   * RHEL
       # sudo yum-config-manager --enable rhel-server-rhscl-7-rpms
2. 安装工具集
   # sudo yum install devtoolset-6
3. 使用软件工具集
   # scl enable devtoolset-6 bash
```

## 说明
```
工具集主要分为
 toolchain 
 perftools
```

## docker使用
```
https://github.com/sclorg/devtoolset-container
```
