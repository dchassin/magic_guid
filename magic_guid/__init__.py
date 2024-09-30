"""Generate a GUID using a magic number

Syntax: mguid [OPTION ...]

Options:

    * -h|--help|help: Display this help information

    * -v|--version|version: Display the mguid version

    * -V|--validate|validate: Run validation tests

    * version=INT: Set the magic trick version (default 0).

    * magic=INT: Set the magic number (default random 60 bit integer).

    * trick=INT[,MAGIC[,VERSION]]: Generate the check code using the magic number
      and the magic trick version.

    * random[=MAGIC]: Generate a magic random GUID

    * check=[GUID[,MAGIC]]: Check whether a GUID is magic

    * same=[GUID,GUID[,MAGIC]]: Check whether two GUIDs are generate with the same
      magic.

Description:

Magic GUIDs contain a pattern that is uniquely identifiable if the magic
number is known.  The `random`_ option generates a Version 4 GUID using a
random magic number. If you know the magic number you can verify that a GUID
was generated with the magic number by using the `check` option.  If you have
two GUIDs, you can verify that they were generated using the same magic
number using the `same` option.

If you do not specify the magic number, a random magic number is generated the
first time you use the `gen()` function, or a function that calls `gen
()`, e.g., `random()` or `validate()`. You can set the magic number using the
`MAGIC` module constant, e.g., `MAGIC=gen()`, `MAGIC=123456`.  

Command Line Examples:

Generate a GUID using the magic number 123.

    $ mguid random=123
    f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af

Check whether the GUID was generated using the magic number 123.

    $ mguid check=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,123 && echo ok || echo fail
    ok

Check whether the GUID was generated using the magic number 456.

    $ mguid check=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,456 && echo ok || echo fail
    fail

Generates another GUID using the magic number 123.

    $ mguid random=123
    2f210452-75be-4d3b-a2f2-1045275bed40

Checks whether the two GUIDs were generated using the same magic number.

    $ mguid same=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,2f210452-75be-4d3b-a2f2-1045275bed40 && echo ok || echo fail
    ok

Generate another GUID using the magic number 456.

    $ mguid random=456
    0a335b25-d565-40fd-80a3-35b25d565135

Check whether the new GUID was generared using the same magic number as the old GUID

    $ mguid same=f2ac57d8-e3e5-45d4-bf2a-c57d8e3e55af,0a335b25-d565-40fd-80a3-35b25d565135 && echo ok || echo fail
    fail

Python Examples:

Import the module.

    >>> import magic_guid as mg

Generate a GUID.

    >>> mg.random()
    0c7d4f21-b322-41183-8086-479cd4100f63e 

Check a GUID.

    >>> mg.check(mg.random())
    True 

Check whether two GUIDs are generated using the same magic number.

    >>> mg.same(mg.random(magic=123),mg.random(magic=123))
    True 

Check whether two GUIDs are generated using the same magic number.

    >>> mg.same(mg.random(magic=123),mg.random(magic=456))
    False 

"""

import sys
import typing
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__name__)
except:
    __version__ = None

VERSION = 0 # 0=magic number is recoverable, 1=magic number is unrecoverable

E_OK = 0
E_ERROR = 1
E_EXCEPTION = 2

MAGIC = None

def gen(bits=60) -> int:
    """Generate a N-bit random number

    Arguments:
        bits (int): the number of bits to generate (default 61)

    Returns:
        int: a N-bit random number
    """
    import random as rg
    if MAGIC is None:
        MAGIC = gen()
    return rg.randint(0,2**bits)

def trick(a:int,magic:int,version:int=None) -> int:
    """Generate the check code using the magic number

    Arguments:
        a (int): the number to run the magic trick on
        magic (int): the magic number to use
        version (int): the version of the magic trick to use (default magic_guid.VERSION)

    Returns:
        int: the result of the magic trick
    """
    if version is None:
        version = VERSION
    if version == 0:
        return a^int(magic)
    if version == 1:
        raise NotImplementedError("version 1 magic tricks not supported yet")
    raise ValueError("invalid magic trick version")

def random(magic:int=None) -> int:
    """Generate a GUID using a magic number

    Arguments:
        magic (int): the magic number to use (default magic_guid.MAGIC)

    Returns:
        int: a magic GUID
    """
    if magic is None:
        magic = MAGIC
    src = gen()
    num = f"{src:015x}"
    chk = f"{trick(src,magic):015x}"
    N = f"{(int(chk[0],16)&3)+8:x}"
    return f"{num[0:8]}-{num[8:12]}-4{num[12:15]}-{N}{chk[0:3]}-{chk[3:]}"

def check(a:str,magic:int=None) -> bool:
    """Check whether a GUID was generated using a magic number

    Arguments:
        a (str): a GUID to test
        magic (int): the magic number to use in the test (default magic_guid.MAGIC)

    Returns:
        bool: True if a was generated using magic, otherwise False
    """
    if magic is None:
        magic = MAGIC
    field = [x for x in a.split("-")]
    if len(field) != 5:
        return False
    if field[2][0] != "4":
        return False
    if field[3][0].lower() not in "89ab":
        return False
    num = int(field[0]+field[1]+field[2][1:],16)
    chk = field[3][1:] + field[4]
    return f"{trick(num,magic):015x}" == chk

def same(a:str,b:str) -> bool:
    """Check whether two GUIDs were generated using the same magic number

    Arguments:
        a (str): the first magic GUID
        b (str): the second magic GUID

    Returns:
        bool: True if a and b were generated using the same magic number
    """
    field = [x for x in a.split("-")]
    if len(field) != 5:
        return False
    if field[2][0] != "4":
        return False
    if field[3][0].lower() not in "89ab":
        return False
    num = int(field[0]+field[1]+field[2][1:],16)
    chk = int(field[3][1:] + field[4],16)
    magic = trick(num,chk)
    return check(b,magic)

def main(argv:[list[str]|None]=None) -> int:
    """Main CLI

    Arguments:
        argv (list[str]): argument list

    Returns:
        int: exit code
    """
    if argv == None:
        argv = list(sys.argv)

    if len(argv) == 1:
        print("\n".join([x for x in __doc__.split("\n") if x.startswith("Syntax: ")]),file=sys.stderr)
        return E_ERROR    
    if argv[1] in ["-h","--help","help"]:
        print(__doc__)
        return E_OK
    if argv[1] in ["-v","--version","version"]:
        print(__version__)
        return E_OK
    if argv[1] in ["-V","--validate","validate"]:
        validate()
        return E_OK
    
    for arg in argv[1:]:
        key,value = arg.split("=",1) if "=" in arg else (arg,None)
        if key == "version":
            VERSION = value
        elif key == "magic":
            MAGIN = value
        elif key in ["random","check","same","gen","trick"]:
            args = value.split(",") if isinstance(value,str) else []
            result = globals()[key](*args)
            if isinstance(result,bool):
                return E_OK if result else E_ERROR
            else:
                print(result)
        else:
            print(arg,"->",key,"=",f"'{value}'")
            raise Exception(f"invalid command argument: '{arg}'")

    return E_OK

def validate():
    """Run validation tests"""
    for n in range(10):
        m = random()
        g = m[:-1]+str((int(m[-1],16)+1)%16)
        p = random()
        q = random(gen())
        assert check(m), f"check('{m}') failed!"
        assert not check(g), f"not check('{g}') failed!"
        assert same(m,p), f"same('{m}','{p}') failed!"
        assert not same(p,q), f"not same('{p}','{q}') failed!"

if __name__ == "__main__":
    try:
        main()
    except:
        e_type,e_value,e_trace = sys.exc_info()
        print(f"ERROR: {e_type.__name__} {e_value}",file=sys.stderr)
 