"""Some exception classes and warning functions"""


def _info(value: str) -> None:
    """Output a piece of information"""
    print(f"\033[36mInfo: {value}\033[0m")


def _warning(value: str) -> None:
    """Output a warning"""
    print(f"\033[33mWarning: {value}\033[0m")


def _error(value: str) -> None:
    """Output an error"""
    print(f"\033[31mError: {value}\033[0m")
