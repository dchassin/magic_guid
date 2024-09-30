docs/index.html: magic_guid/__init__.py
	test -d .venv || python3 -m venv .venv
	(source .venv/bin/activate; python3 -m pip install . ; python3 utils/quickdocs.py)
