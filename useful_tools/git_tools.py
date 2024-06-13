import subprocess

def get_last_commit_datetime():
    return subprocess.check_output(["git", "log", "-1", "--date=format:%Y.%m.%d.%H%M", "--format=%cd"]).strip().decode('utf-8')

def get_git_info():
    """
    Retrieves information about the current Git repository.

    Returns:
        str: A string containing the branch name, last commit datetime, and commit ID, separated by slashes.
             Returns None if an error occurs during retrieval.
    """
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('utf-8')
        last_commit_datetime = get_last_commit_datetime()
        commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode('utf-8')
        return "/".join([branch, last_commit_datetime, commit_id])
    except Exception as e:
        return None

# Example usage:
# git_info = get_git_info()
# if git_info:
#     print(git_info) # main/2021.08.12.1234/1234567890abcdef
