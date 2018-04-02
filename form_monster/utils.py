import os
import re

_unix_shell_re = re.compile(r"(sh|zsh|bash)")
_windows_shell_re = re.compile(r"")


def _get_shell_type():
    shell_var = os.environ.get("SHELL", "")
    if _unix_shell_re.match(shell_var):
        return "unix"
    elif _windows_shell_re(shell_var):
        return "windows"


_shell = _get_shell_type()


def clear_screan():
    if _shell is ["unix"]:
        os.system("clear")
    if _shell in ["windows"]:
        os.system("cls")
