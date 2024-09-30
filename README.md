[![validate-main](https://github.com/dchassin/magic_guid/actions/workflows/validate-main.yml/badge.svg?branch=main)](https://github.com/dchassin/magic_guid/actions/workflows/validate-main.yml)
[![pages-build-deployment](https://github.com/dchassin/magic_guid/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/dchassin/magic_guid/actions/workflows/pages/pages-build-deployment)
[![Publish PyPI](https://github.com/dchassin/magic_guid/actions/workflows/publish-tagged.yml/badge.svg)](https://github.com/dchassin/magic_guid/actions/workflows/publish-tagged.yml)
Magic GUIDs contain a pattern that is verifiable if the magic number is known.  Two magic GUIDs can be compared to check if they were generated using the same magic number.

Installation
------------

To install from a repository

~~~
git clone https://github.com/dchassin/magic_guid
python3 -m pip install magic_guid
~~~

Command Line Help
-----------------

~~~
mguid help
~~~

Documentation
-------------

See https://www.chassin.org/magic_guid/ for online documentation.


Contributions
-------------

The implementation code is located in `magic_guid/__init__.py`.

After updating the code, you must update and push the documentation using the `Makefile`, e.g.

~~~
$ make
~~~
