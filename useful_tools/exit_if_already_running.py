import os
import sys
import psutil
from datetime import datetime

def exit_if_already_running(pid_file, verbose=False):
    """
    Check if the script is already running by checking the PID in the pid file.
    If the script is already running, exit the program.

    Args:
        pid_file (str): The path to the PID file.
        verbose (bool, optional): If True, print verbose messages. Defaults to False.
    """
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as pidfile:
            try:
                pid = int(pidfile.read())
            except ValueError:
                print(f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')} Error reading the PID from {pid_file} - exiting...")
                sys.exit(1)
        try:
            if psutil.pid_exists(pid):
                if verbose:
                    print(f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')} The script is already running with PID {pid} - exiting...")
                sys.exit(0)
        except psutil.NoSuchProcess:
            pass
    with open(pid_file, "w") as pidfile:
        pidfile.write(str(os.getpid()))
        if verbose:
            print(f"{datetime.now().strftime('%Y.%m.%d %H:%M:%S')} Script is not already running - PID written to {pid_file}")
    return
