GIT_TAG := $(shell git describe --tags)

.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: build-src-release
build-src-release:
	@mkdir -p releases
	@zip -r "releases/base-project-$(GIT_TAG).zip" game license