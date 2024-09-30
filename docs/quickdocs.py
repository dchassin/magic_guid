"""Generate ../index.html

You must install the module in .venv to generate the docs.

The generate the docs run this script.
"""
import magic_guid as module
import re

package = module.importlib.metadata.distribution(module.__name__).metadata
package_name = package['name'].replace('_',' ').title()

with open("../index.html","w") as html:

    def write_html(text,md=True,nl=False):
        if md:
            rules = {
                r"`(.+)`": r"<code>\1</code>",
                r"\*\*(.+)\*\*": r"<b>\1</b>",
                r"\*(.+)\*": r"<i>\1</i>",
                r"~(.+)~": r"<u>\1</u>",
                r"_(.+)_": r"<sub>\1</sub>",
                r"\^(.+)\^": r"<sup>\1</sup>",
                r"([a-z]+)://([A-Za-z0-9/.:@+_?&]+)": r"""<a href="\1://\2" target="_tab">\1://\2</a>""",
            }
            for search,replace in rules.items():
                text = re.sub(search,replace,text)
        html.write(text)
        if nl:
            html.write("\n")

    mode = None

    def set_mode(m):
        global mode
        if mode and mode != m:
            html.write(f"</{mode}>\n")
            mode = None
        if m and m != mode:
            mode = m
            html.write(f"<{mode}>")

    write_html(f"""<!doctype html>
<html>
<head>
    <title>{package_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<h1>{package_name}</h1>
""",nl=True)
    for line in module.__doc__.split("\n"):
        if len(line) == 0:
            if mode is None:
                html.write("<p/>")
        elif line.startswith("Syntax: "):
            write_html(f"Syntax: <code>{line[8:]}</code>")
        elif line.endswith(":"):
            set_mode(None)
            write_html(f"\n<h2>{line[:-1]}</h2>\n")
        elif line.startswith("    * "):
            set_mode("ul")
            line = line[6:]
            if ":" in line:
                part = line.split(":",1)
                html.write(f"</li>\n<li><code>{part[0]}</code>: {part[1]}")
            else:
                html.write(f"</li>\n<li>{line}")
        elif line.startswith("      "):
            write_html(f"{line[5:]}")
        elif line.startswith("    "):
            set_mode("pre")
            write_html(f"{line[4:]}\n")
        else:
            set_mode(None)
            write_html(f"{line}\n")

    set_mode(None)
    write_html("\n<h1>Python Documentation</h1>\n")

    for name in dir(module):
        set_mode(None)
        if name.startswith("__"):
            continue
        value = getattr(module,name)
        if callable(value):
            if isinstance(value.__doc__,str):
                write_html(f"\n<h2>{name}(")
                write_html(", ".join([f"<b>{str(a)}</b>:<i>{b.__name__ if hasattr(b,"__name__") else str(b)}</i>" for a,b in value.__annotations__.items() if a != "return"]))
                write_html(")")
                if hasattr(value,"return"):
                    c = value.__annotations__["return"]
                    write_html(f" -> {c.__name__ if hasattr(c,"__name__") else str(c)}")
                write_html("</h2>\n")
                
                for line in value.__doc__.split("\n"):
                    if len(line) == 0:
                        if mode is None:
                            html.write("<p/>")
                    elif line.startswith("    ") and line.endswith(":"):
                        set_mode(None)
                        html.write(f"<h3>{line.strip()}</h3>\n")
                    elif line.startswith("        "):
                        set_mode("ul")
                        part = line.strip().split(":",1)
                        if len(part) == 2:
                            html.write(f"<li><code>{part[0]}</code>: {part[1]}</li>\n")
                        else:
                            html.write(f"<li>{part[0]}</li>\n")
                    else:
                        set_mode(None)
                        write_html(f"{line}\n")
            else:
                print(f"WARNING: function '{name}' has no __doc__")
        set_mode(None)

    constant_header = False
    for name in dir(module):
        if name.startswith("__"):
            continue
        value = getattr(module,name)
        if type(value) in [int,float,list,dict,str] or value is None:
            if not constant_header:
                html.write("<h2>Python Constants</h2>")
                constant_header = True
            write_html(f"<p/><code>{name} = {value}</code>")

    write_html("\n<h1>Package Metadata</h1>\n")
    write_html("<table>\n")
    for key,data in package.items():
        if not key.startswith("Description"):
            write_html(f"<tr><th><nobr>{key.title()}</nobr></th><td>{data}</td></tr>")
    write_html("</table>\n")

    write_html("""</body>
        </html>""",nl=True)
