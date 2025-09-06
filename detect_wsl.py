import platform, sys, functools, shutil
import os.path

# https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on/58071295#58071295
@functools.cache
def get_os_type():
    #'Windows', 'Linux' or 'Darwin'
    return platform.system()
@functools.cache
def get_os_name():
    #'win32', 'win16', 'linux', 'linux2', 'darwin', 'freebsd8', etc
    #Calls OS-specific APIs to get the OS name as defined by the OS
    return sys.platform

# https://askubuntu.com/questions/1177729/wsl-am-i-running-version-1-or-version-2
@functools.cache
def is_os_wsl(os_release: str = None):
    if get_os_type() != 'Linux':
        return False
    os_release = platform.uname().release if os_release is None else os_release
    return (os_release.endswith('Microsoft') or
            os_release.endswith('microsoft-standard-WSL2'))

@functools.cache
def get_win32_process_ancestry():
    if get_os_name() != 'win32':
        raise OSError('This function only works on Win32 systems')
    from win32_process_parents import get_windows_pid, get_all_parent_names
    my_pid = get_windows_pid()
    ancestry = get_all_parent_names(my_pid)
    return ancestry

def detect_launch_from_wsl():
    if get_os_name() == 'win32':
        ancestry = get_win32_process_ancestry()
        return any('WSL\\wsl.exe' in path for path in ancestry)
    return False

def is_wsl_installed():
    return get_os_name() == 'win32' and shutil.which("wsl")

def get_OS_environment():
    return OS_environment_record(
        get_os_type(),
        get_os_name(),
        is_os_wsl(),
        platform.uname(),
        detect_launch_from_wsl()
    )

class OS_environment_record:
    def __init__(self, os_type, os_name, is_wsl_python,
                 uname_result, is_win32_launched_from_wsl):
        self.os_type = os_type
        self.os_name = os_name
        self.is_wsl_python = is_wsl_python
        self.uname_result = uname_result
        self.is_win32_launched_from_wsl = is_win32_launched_from_wsl

    def __repr__(self):
        return (
            'OS_environment_record('
            + ', '.join(
                (f'{varname}={self.__dict__[varname]}'
                 for varname in self.__dict__)
            )
            + ')'
        )

    def explain(self):
        explanation = []
        explanation.append(f'Python is running in {self.os_type} ({self.os_name})')
        explanation.append(f'with release "{self.uname_result.release}", '
                           f'version "{self.uname_result.version}", '
                           f'compiled for {self.uname_result.machine}')
        if self.is_wsl_python:
            explanation.append('(This is a WSL instance on a Windows machine)')
        elif self.is_win32_launched_from_wsl:
            explanation.append('But this instance was launched from inside WSL:')
            ancestry = reversed(get_win32_process_ancestry()) #reverse so python.exe is last
            explanation.append(' -> '.join(os.path.basename(path) for path in ancestry))
        elif self.os_name == 'win32':
            if is_wsl_installed():
                explanation.append('WSL appears to be installed but is not being '
                                   'used by this Python instance')
            else:
                explanation.append('WSL is not installed')
        return '\n'.join(explanation)
        



