# Makefile
#
# You must run this after updating the code to ensure the documentation is updated as well
#

docs/index.html: magic_guid/__init__.py Makefile utils/quickdocs.py
	@test -d .venv || python3 -m venv .venv
	@echo Updating $@...
	(source .venv/bin/activate; python3 -m pip install . ; python3 utils/quickdocs.py)
	@echo Done
