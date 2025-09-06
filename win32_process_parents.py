import ctypes
from ctypes.wintypes import DWORD, LONG, MAX_PATH

# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32first
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
# https://stackoverflow.com/questions/29939893/get-parent-process-name-windows

kernel32 = ctypes.WinDLL('kernel32')

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', DWORD),
                ('cntUsage', DWORD),
                ('th32ProcessID', DWORD),
                ('th32DefaultHeapID', ctypes.c_void_p),
                ('th32ModuleID',  DWORD),
                ('cntThreads', DWORD),
                ('th32ParentProcessID', DWORD),
                ('pcPriClassBase', LONG),
                ('dwFlags', DWORD),
                ('szExeFile', ctypes.c_char * MAX_PATH)]

def get_parent_pid(pid):
    # The flag 0x2 means take a snapshot of all processes
    snapshot_handle = kernel32.CreateToolhelp32Snapshot(0x2, 0)

    lppe = PROCESSENTRY32()
    lppe.dwSize = ctypes.sizeof(lppe)

    success = kernel32.Process32First(snapshot_handle, ctypes.pointer(lppe))
    if success:
        if lppe.th32ProcessID == pid:
            return (0, lppe.th32ParentProcessID)
        else:
            while kernel32.Process32Next(snapshot_handle, ctypes.pointer(lppe)):
                if lppe.th32ProcessID == pid:
                    return (0, lppe.th32ParentProcessID)
    return (kernel32.GetLastError(), 0)

def get_process_name(pid):
    # 0x1000: PROCESS_QUERY_LIMITED_INFORMATION
    process_handle = kernel32.OpenProcess(0x1000, 0, pid)
    if process_handle:
        #assume each utf-16 character is 2 bytes (TODO: is this safe?)
        name = ctypes.create_string_buffer(MAX_PATH*2)
        size = ctypes.c_uint64(MAX_PATH*2)
        if kernel32.QueryFullProcessImageNameW(process_handle, 0, name, ctypes.pointer(size)):
            python_name = bytes(name).decode('utf-16')
            return (0, python_name[:python_name.index('\x00')])
    return (kernel32.GetLastError(), '')

def get_all_parent_names(pid):
    '''Get the paths to the executables of the Python process,
    its parent process, and so on'''
    pids = []
    error = 0
    while not error:
        pids.append(pid)
        error, pid = get_parent_pid(pid)
    names = []
    for pid in pids:
        error, name = get_process_name(pid)
        if error:
            break
        names.append(name)
    return names

def get_windows_pid():
    '''Get the Process ID of the Python process from the Windows kernel'''
    return kernel32.GetCurrentProcessId()

### DEBUG CODE BELOW
##
##class CannotContinue(Exception):
##    pass
##
##if __name__ == '__main__':
##
##    try:
##        my_pid = get_windows_pid()
##        print('My PID:', my_pid)
##        error, my_process_name = get_process_name(my_pid)
##        if error: print('Error', error); raise CannotContinue
##        print('My process name:', my_process_name)
##        pid = my_pid
##        for i in range(3):
##            print()
##            error, pid = get_parent_pid(pid)
##            if error: print('Error', error); raise CannotContinue
##            print('Parent PID:', pid)
##            error, parent_process_name = get_process_name(pid)
##            if error: print('Error', error); raise CannotContinue
##            print('Parent process name:', parent_process_name)
##
##    except CannotContinue:
##        pass
