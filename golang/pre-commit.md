# pre-commit hook

## 安装pre-commit
```
sudo dnf -y install pre-commit
```

## 配置
```
在项目根目录创建： .pre-commit-config.yaml
基本项示例:
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: trailing-whitespace  // 处理行尾和新行的任何空格
      - id: end-of-file-fixer // 删除项目文件中的EOF
      - id: check-yaml // 修复yaml格式文件
      - id: check-added-large-files // 检查大文件

golang的示例:
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.0
    hooks:
      - id: go-fmt // go-fmt格式化项目
      - id: go-imports // 更新import
      - id: no-go-testing // 查找并警告哪些文件没有测试覆盖
      - id: golangci-lint // 运行linter
      - id: go-unit-tests // 运行go test命令

完整示例:
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.0
    hooks:
      - id: go-fmt
      - id: go-imports
      - id: no-go-testing
      - id: golangci-lint
      - id: go-unit-tests
      # - id: validate-toml
  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v8.0.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
        additional_dependencies: ['@commitlint/config-conventional']
```

## ref
[Golang: Improving your GO project With pre-commit hooks](https://goangle.medium.com/golang-improving-your-go-project-with-pre-commit-hooks-a265fad0e02f)
[Conventional Commits](https://www.conventionalcommits.org/)
[pre-commit](https://pre-commit.com/)
[语义化版本](https://semver.org/lang/zh-CN/)
[Golang CI Lint](https://golangci-lint.run)
[gogolf-template](https://github.com/iamgoangle/gogolf-template)
