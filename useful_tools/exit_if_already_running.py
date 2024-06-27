import os
import sys
import psutil
import signal
from datetime import datetime

def is_process_running(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL 
    except OSError:
        return f"Error: No process with PID {pid} exists"
    else:
        return f"Process successfully killed process with PID {pid}"

def exit_if_already_running(pid_file, verbose=False, timestamp=False):
    """
    Check if the script is already running by checking the PID in the pid file.
    If the script is already running, exit the program.

    Args:
        pid_file (str): The path to the PID file.
        verbose (bool, optional): If True, print verbose messages. Defaults to False.
    """
    my_pid = os.getpid()
    if os.path.isfile(pid_file):
        timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S') if timestamp else ""
        with open(pid_file, "r") as pidfile:
            try:
                pid = int(pidfile.read())
            except ValueError:
                print(f"{timestamp}[PID {my_pid}] Error reading the PID from {pid_file} - exiting...")
                sys.exit(1)
        if is_process_running(pid):
            if verbose:
                print(f"{timestamp}[PID {my_pid}] The script is already running with PID {pid} - exiting...")
            sys.exit(0)
        else:
            if verbose:
                print(f"{timestamp}[PID {my_pid}] The process with PID {pid} is not running - removing {pid_file}")
            os.remove(pid_file)
    with open(pid_file, "w") as pidfile:
        pidfile.write(str(os.getpid()))
        if verbose:
            print(f"{timestamp}[PID {my_pid}] No other script is running - PID written to {pid_file}")
    return
