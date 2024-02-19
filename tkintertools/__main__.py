"""
Entry point of the tkt-designer

Use command bellow to start tkt-designer:

```bash
python -m tkintertools [options]
```

On some OS, maybe should use command bellow:

```bash
python3 -m tkintertools [options]
```
"""

import sys

if __name__ == "__main__":
    from . import designer
    designer.run(*sys.argv)
