import os
import re
import logging
import subprocess
import sys

log = logging.getLogger()

UNIX_SHELL_RE = re.compile(r".*(sh|zsh|bash).*")
WINDOWS_SHELL_RE = re.compile(r".*(PS).*")


def get_current_environment():
    shell_var = os.environ.get("SHELL", "")
    if UNIX_SHELL_RE.match(shell_var):
        return "unix"
    elif WINDOWS_SHELL_RE.match(shell_var):
        return "windows"
    else:
        log.warn("Unable to detect working environment")


environment = get_current_environment()


def clear_screan():
    if environment in ["unix"]:
        sys.stderr.write("\x1b[2J\x1b[H")
        # os.system("clear")
    if current_shell in ["windows"]:
        os.system("cls")
