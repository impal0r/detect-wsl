# Detect whether python is inside WSL

Sometimes, it matters whether you are running the native Windows version of Python, or the one installed inside WSL (Windows Subsystem for Linux). Sometimes, it also matters whether you are running the native installation from inside WSL (programs like python.exe installed on the host machine are accessible from inside WSL and you can run them). If you want to modify the clipboard to copy something, for example, the default method doesn't work from inside WSL even if you're running python.exe.

Now, Python can figure it out for you.

This tool checks in the usual places (`platform.uname()`, `sys.platform`) to figure out which OS Python is running in. If the OS is a Linux distro, it checks the OS version name to see if it's WSL-flavoured. If the OS is Windows, it looks up Python's parent processes to see if WSL is one of them.

This covers all possible cases on a Windows computer, and has the upshot of telling you which chain of process parents ended up spawning the currently running Python instance - potentially a useful debug tool.

### Installation

You can install detect-wsl from TestPyPI:

```
pip install -i https://test.pypi.org/simple/ detect-wsl
```

Works on: Python 3.6+
- format-string syntax was introduced in Python 3.6
- you might get some warnings in Python 3.6~3.8, but the code worked on my machine

Fully supported python versions: 3.9+
- result caching supported, which speeds up subsequent calls to the functions in detect_wsl (using `functools.cache`)

### How to use

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

### Human-readable output

On the command line:
```
python -m detect_wsl
```

In your code:
```py
from detect_wsl import get_OS_environment
print(get_OS_environment().explain())
```
-> (e.g.)
```
Python is running in Windows (win32)
with release "10", version "10.0.19045", compiled for AMD64
But this script was launched from inside WSL:
explorer.exe -> wsl.exe -> python.exe
```