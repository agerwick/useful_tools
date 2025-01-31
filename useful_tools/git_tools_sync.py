import subprocess
import asyncio

class GitInfoError(RuntimeError):
    """Exception raised for errors in the retrieval of Git information."""
    pass

def in_async_context():
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

def run_git_command(command):
    if in_async_context():
        raise RuntimeError("useful_tools/git_tools is not meant to be called in an async context. Use useful_tools/git_tools_async instead.")
        # reason: when you call subprocess in debug mode (debugpy), it will hang in most cases.
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT).strip().decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        """Fix for this error, which occurs when the repository is owned by a different user (on Windows):
        Error: fatal: detected dubious ownership in repository at 'C:/code/my-codebase'
        'C:/code/my-codebase' is owned by:
                AzureAD/UserThatOwnsDir (S-1-12-x-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxx-xxxx)
        but the current user is:
                COMPUTERNAME/UserScriptIsRunningAs (S-1-5-x-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxx-xxxx)
        To add an exception for this directory, call:

                git config --global --add safe.directory C:/code/my-codebase

        """
        if "detected dubious ownership in repository" in output: # pragma: no cover
            # Extract the directory path from the error message
            directory = output.split("'")[1] # get the text between the first two single quotes
            # Add the directory to the safe list
            subprocess.check_output(["git", "config", "--global", "--add", "safe.directory", directory])
            # Retry the original command
            return subprocess.check_output(command, stderr=subprocess.STDOUT).strip().decode('utf-8')
        else:
            raise e

def get_last_commit_datetime():
    return run_git_command(["git", "log", "-1", "--date=format:%Y.%m.%d.%H%M", "--format=%cd"])

def get_current_branch():
    return run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])

def get_commit_id():
    return run_git_command(["git", "rev-parse", "HEAD"])

def get_git_info():
    """
    Retrieves information about the current Git repository.

    Returns:
        str:    A string containing the branch name, last commit datetime, and commit ID, separated by slashes.
                Returns an error message if an error occurs during retrieval.
    """
    try:
        branch = get_current_branch()
        last_commit_datetime = get_last_commit_datetime()
        commit_id = get_commit_id()
        return "/".join([branch, last_commit_datetime, commit_id])
    except subprocess.CalledProcessError as e:
        raise GitInfoError(f"Error getting git info:\n{e.output.decode('utf-8')}")
    except Exception as e:
        raise GitInfoError(f"Unexpected error getting git info:\n{str(e)}")

# Example usage:
# git_info = get_git_info()
# if git_info:
#     print(git_info) # main/2021.08.12.1234/1234567890abcdef or Error: <error message>