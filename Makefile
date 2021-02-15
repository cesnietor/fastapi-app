TAG ?= "python_dev_case"

default: docker

docker:
	@echo 'Building docker image...'
	@docker build -t $(TAG) .

test:
	@echo 'Running unit tests...'
	@pytest -v