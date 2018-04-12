from .utils import UNIX_SHELL_RE, WINDOWS_SHELL_RE


def test_unix_shell_regex():
    result = UNIX_SHELL_RE.match("/usr/bin/zsh")
    assert result, "should return a value"

    result = UNIX_SHELL_RE.match("/usr/bin/powershell")
    assert result, "should return a value"


def test_windows_shell_regex():
    result = WINDOWS_SHELL_RE.match("/usr/bin/zsh")
    assert result is None
