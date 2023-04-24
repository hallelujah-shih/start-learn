# git

## git workflow
```
核心常存分支： master、develop
要点： 从哪儿来，回哪儿去
```

### 创建feature branch
```
git checkout -b myfeature develop
# git switch -c <new-branch-name>
```

### develop分支上合并一个完成的特性
```
git checkout develop
git merge --no-ff myfeature
git branch -d myfeature
git push origin develop
```

### 创建一个发布分支
```
git checkout -b release-1.2 develop
git commit -a -m "xxxxx"
```

### 完成一个发布分支
```
git checkout master
git merge --no-ff release-1.2
git tag -a 1.2

# 在develop分支shanghai保留发布分支的更改
git checkout develop
git merge --no-ff release-1.2

# 清理
git branch -d release-1.2
```

## git submodules
```
子模块的操作
```

### 使用包含子模块的存储库
```
1. 克隆包含子模块的仓库
    1.1 git clone时候附带克隆子模块
        git clone --recursive [URL to Git repo]
    1.2 仓库已经存在并进行更新
        1.2.1 无嵌套更新
            git submodule update --init
        1.2.2 嵌套更新
            git submodule update --init --recursive

2. 并行下载子模块
    仓库不存在时：
        git clone --recursive --jobs 8 [URL to Git repo]
    仓库存在时：
        git submodule update --init --recursive --jobs 8

3. 子模块拉取（pull）
    3.1 同时更新仓库以及子模块的改动
        git pull --recurse-submodules
    3.2 拉取子模块中的所有改动
        git submodule update --remote

4. 在每个子模块上执行命令
    4.1 不嵌套操作
        git submodule foreach 'git reset --hard'
    4.2 嵌套操作
        git submodule foreach --recursive 'git reset --hard'
```

### 使用子模块创建存储库
```
1. 将子模块添加到仓库
    // add
    git submodule add -b <branch> [URL to Git repo]
    如：git submodule add -b master --depth 1 https://github.com/tezc/sc.git third_party/sc
    // init
    git submodule init

2. 子模块更新
    git submodule update --remote

3. 子模块删除
    git submodule deinit -f -- third_party/sc
    rm -rf .git/modules/third_party/sc
    git rm -f third_party/sc
```

### 变更子模块的url或branch
```
# 查看子模块相关信息
git config --file=.gitmodules -l

submodule.third_party/sc.path=third_party/sc
submodule.third_party/sc.url=https://github.com/tezc/sc.git
submodule.third_party/sc.branch=master


# 新一点的git
## 更新submodule的url路径
git submodule set-url third_party/sc https://github.com/test/sc.git
## 更新分支
git submodule set-branch -b dev third_party/sc

# 老点的git
## 更新submodule的url路径
git config --file=.gitmodules submodule.third_party/sc.url https://github.com/tezc/sc.git
## 更新分支
git config --file=.gitmodules submodule.third_party/sc.branch master

git submodule sync
make update

## 清理子模块
    所有:
        git submodule deinit -f --all
    指定清理:
        git submodule deinit -f -- third_party/sc
```

## ref
* [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
* [Using submodules in Git - Tutorial](https://www.vogella.com/tutorials/GitSubmodules/article.html)
* [How to Change the Remote Repository for a Git Submodule?](https://linuxhint.com/change-the-remote-repository-for-a-git-submodule/)
