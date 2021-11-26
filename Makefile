.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help: ## Print all commands.
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

preview: ## Preview a visualization. Select the visualization using 'name=...'
	sudo python3 -m backend.preview --name $(name) 

run: ## Initialize and run the frontend and backend servers.
	cd ~/PiLights/frontend; serve -l 3000 -s build &
	cd ~/PiLights/backend; sudo -E flask run --host=192.168.7.99
