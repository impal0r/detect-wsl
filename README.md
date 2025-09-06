# Detect whether python is inside WSL

Sometimes, it matters whether you are running the native Windows version of Python, or the one installed inside WSL (Windows Subsystem for Linux). Sometimes, it also matters whether you are running the native version from inside WSL (e.g. you want to modify the clipboard).

Now, Python can figure it out for you.

This script checks in the usual places (`platform.uname()`, `sys.platform`) to figure out which OS Python is running under. Then, it checks the OS version name to check if it's WSL on Linux, and finds Python's parent processes on Windows to see if WSL is one of them.

### Usage

```py
from detect_wsl import get_OS_environment

env = get_OS_environment()

if env.is_os_wsl:
    print('You are running a Linux version of Python installed inside WSL')
if env.os_type == 'Windows':
    if env.is_win32_launched_from_wsl:
        print('You are running a Windows version of Python from inside WSL')
    else:
        print('You are running a Windows version of Python from outside WSL')
```

### Human-readable interface

```py
from detect_wsl import get_OS_environment
print(get_OS_environment().explain())
```
-> (e.g.)
```
Python is running in Windows (win32)
with release "10", version "10.0.19045", compiled for AMD64
WSL appears to be installed but is not being used by this Python instance
```