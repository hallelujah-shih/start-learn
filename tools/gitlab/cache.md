# cache

## template
```
# You can copy and paste this template into a new `.gitlab-ci.yml` file.
# You should not add this template to an existing `.gitlab-ci.yml` file by using the `include:` keyword.
#
# To contribute improvements to CI/CD templates, please follow the Development guide at:
# https://docs.gitlab.com/ee/development/cicd/templates.html
# This specific template is located at:
# https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Go.gitlab-ci.yml

image: golang:latest

.go-cache:
  variables:
    GOPATH: $CI_PROJECT_DIR/.go
  before_script:
    - mkdir -p .go
  cache:
    paths:
      - .go/pkg/mod/

stages:
  - test
  - build
  - deploy

format:
  stage: test
  extends: .go-cache
  script:
    - go fmt $(go list ./... | grep -v /vendor/)
    - go vet $(go list ./... | grep -v /vendor/)
    - go test -race $(go list ./... | grep -v /vendor/)

compile:
  stage: build
  extends: .go-cache
  script:
    - mkdir -p mybinaries
    - go build -o mybinaries ./...
  artifacts:
    paths:
      - mybinaries

deploy:
  stage: deploy
  extends: .go-cache
  script: echo "Define your deployment script!"
  environment: production

```

## ref
* [golang cache](https://docs.gitlab.com/ee/ci/caching/#cache-go-dependencies)
* [Gitlab CI/CD 实践四：Golang 项目 CI/CD 流水线配置](https://cloud.tencent.com/developer/article/2115054)