# git workflow
```
核心常存分支： master、develop
要点： 从哪儿来，回哪儿去
```

## 创建feature branch
```
git checkout -b myfeature develop
```

## develop分支上合并一个完成的特性
```
git checkout develop
git merge --no-ff myfeature
git branch -d myfeature
git push origin develop
```

## 创建一个发布分支
```
git checkout -b release-1.2 develop
git commit -a -m "xxxxx"
```

## 完成一个发布分支
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

## ref
* [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)