Generate a GUID that conforms to a magic number

Syntax: mguid [OPTION ...]

Options
-------

* -h|--help|help: Display this help information

* -v|--version|version: Display the mguid version

* version=INT: Set the magic trick version (default 0).

* magic=INT: Set the magic number (default random 61 bit integer).

* trick=NUM[,MAGIC[,VERSION]]: Generate the check code using the magic number
  and the magic trick version.

* random[=MAGIC]: Generate a magic random GUID

* check=[NUM[,MAGIC]]: Check whether a GUID is magic

* same=[NUM,NUM[,MAGIC]]: Check whether two GUIDs are generate with the same
  magic.

Description
-----------

Magic GUIDs contain a pattern that uniquely identifiable if the magic trick is
known.  The `random` option generates a Version 4 GUID using a random magic
trick. If you know the magic trick you can verify that a GUID was generated
with the trick by using the `check` option.  If you have two GUIDs, you
can verify that they were generated using the same magic trick using the
`same` option.

Command Line Examples
---------------------

    $ mguid random=123
    f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af

    $ magic_guid david$ mguid check=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,123 && echo ok || echo fail
    ok

    $ mguid check=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,456 && echo ok || echo fail
    fail

    $ mguid random=123
    2f210452-75be-4d3b-a2f2-1045275bed40

    $ mguid same=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,2f210452-75be-4d3b-a2f2-1045275bed40 && echo ok || echo fail
    ok

    $ mguid random=456

    0a335b25-d565-40fd-80a3-35b25d565135
    $ mguid same=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,0a335b25-d565-40fd-80a3-35b25d565135 && echo ok || echo fail
    fail

Python Examples
---------------

    >>> from magic_guid import random, check, same
    >>> random()
    0c7d4f21-b322-41183-8086-479cd4100f63e 

    >>> check(random())
    True 

    >>> same(random(magic=123),random(magic=123))
    True 

    >>> same(random(magic=123),random(magic=456))
    False 


