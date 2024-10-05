# Makefile
#
# You must run this after updating the code to ensure the documentation is updated as well
#

docs/index.html: mguid.py Makefile
	@test -d .venv || python3 -m venv .venv
	@echo Updating $@...
	(source .venv/bin/activate; python3 -m pip install -r requirements.txt)
	(source .venv/bin/activate; pylint mguid.py)
	(source .venv/bin/activate; export PYTHONPATH=.; qdox --withcss)
	@echo Done
