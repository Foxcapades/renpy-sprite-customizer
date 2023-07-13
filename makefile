GIT_TAG := $(shell git describe --tags)

.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: build-src-release
build-src-release:
	@mkdir -p releases
	@zip -r "releases/base-project-$(GIT_TAG).zip" game license

.PHONY: build-docs
build-docs:
	@asciidoctor -b html5 -o docs/index.html docs/index.adoc