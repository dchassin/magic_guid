[![validate-main](https://github.com/dchassin/magic_guid/actions/workflows/validate-main.yml/badge.svg?branch=main)](https://github.com/dchassin/magic_guid/actions/workflows/validate-main.yml)
[![pages-build-deployment](https://github.com/dchassin/magic_guid/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/dchassin/magic_guid/actions/workflows/pages/pages-build-deployment)
[![Publish PyPI](https://github.com/dchassin/magic_guid/actions/workflows/publish-tagged.yml/badge.svg)](https://github.com/dchassin/magic_guid/actions/workflows/publish-tagged.yml)

Magic GUIDs contain a pattern that is verifiable if the magic number is known.  Two magic GUIDs can be compared to check if they were generated using the same magic number.

Installation
------------

To install from a repository

    python3 -m pip install git+https://github.com/eudoxys/mguid

Documentation
-------------

See https://www.eudoxys.com/mguid/ for online documentation.

Shell Usage
-----------

Command line help:

    mguid help

Create a magic GUID:

    mguid random

Create a GUID using a magic number

    mguid random=123

Compare magic GUIDs

    a=$(mguid random=123)
    echo $a
    b=$(mguid random=123)
    echo $b
    c=$(mguid random=456)
    echo $c
    mguid same=$a,$b && echo yes || echo no
    mguid same=$a,$c && echo yes || echo no

Python Usage
------------

Import the module

    import mguid

Generate a magic GUID:

    mg.random()

Check a magic GUID:

    mg.check(mg.random())

Compare two magic GUIDs:

    mg.same(mg.random(123),mg.random(123))
    mg.same(mg.random(123),mg.random(456))

Contributions
-------------

The implementation code is located in `mguid.py`.

After updating the code, you must update and push the documentation using the `Makefile`, e.g.

    make
    git commit -a -m "Updated code"
    git push
