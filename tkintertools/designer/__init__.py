"""
tkt-designer
"""
import sys

from . import main


def run(**kw) -> None:
    """Start tkt designer"""
    main.Application(*sys.argv[1:], **kw).root.mainloop()
