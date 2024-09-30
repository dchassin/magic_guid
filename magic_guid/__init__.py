"""Generate a GUID that conforms to a magic number

Syntax: `mguid [OPTION ...]`

Options
-------

`-h|--help|help`: Display this help information

`-v|--version|version`: Display the mguid version

`-V|--validate|vadliate`: Run validation tests

`version=INT`: Set the magic trick version (default 0).

`magic=INT`: Set the magic number (default random 61 bit integer).

`trick=INT[,MAGIC[,VERSION]]`: Generate the check code using the magic number
  and the magic trick version.

`random[=MAGIC]`: Generate a magic random GUID

`check=[GUID[,MAGIC]]`: Check whether a GUID is magic

`same=[GUID,GUID[,MAGIC]]`: Check whether two GUIDs are generate with the same
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

"""

import sys
import typing
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__name__)
except:
    __version__ = None

VERSION = 0 # 0=magic number is recoverable, 1=magic number is unrecoverable

def gen(bits=60) -> int:
    """Generate a N-bit random number

    Arguments:
        bits (int): the number of bits to generate (default 61)

    Returns:
        int: a N-bit random number
    """
    import random as rg
    return rg.randint(0,2**bits)

E_OK = 0
E_ERROR = 1
E_EXCEPTION = 2

MAGIC = gen()

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

def main(argv:[list|None]=None) -> int:
    """Main CLI

    Arguments:
        argv (list[str])

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
 