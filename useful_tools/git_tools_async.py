# identical to useful_tools/git_tools.py, but for use in an async context, such as in FastAPI

import asyncio

class GitInfoError(RuntimeError):
    """Exception raised for errors in the retrieval of Git information."""
    pass

async def run_git_command(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        output = stderr.decode('utf-8')
        if "detected dubious ownership in repository" in output:
            # Extract the directory path from the error message
            directory = output.split("'")[1] # get the text between the first two single quotes
            # Add the directory to the safe list
            await asyncio.create_subprocess_exec("git", "config", "--global", "--add", "safe.directory", directory)
            # Retry the original command
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                raise GitInfoError(stderr.decode('utf-8'))
        else:
            raise GitInfoError(stderr.decode('utf-8'))
    return stdout.decode('utf-8').strip()

async def get_last_commit_datetime():
    return await run_git_command(["git", "log", "-1", "--date=format:%Y.%m.%d.%H%M", "--format=%cd"])

async def get_current_branch():
    return await run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])

async def get_commit_id():
    return await run_git_command(["git", "rev-parse", "HEAD"])

async def get_git_info():
    """
    Retrieves information about the current Git repository.

    Returns:
        str:    A string containing the branch name, last commit datetime, and commit ID, separated by slashes.
                Returns an error message if an error occurs during retrieval.
    """
    try:
        last_commit_datetime = await get_last_commit_datetime()
        branch = await get_current_branch()
        commit_id = await get_commit_id()
        return "/".join([branch, last_commit_datetime, commit_id])
    except Exception as e:
        raise GitInfoError(f"Error getting git info:\n{str(e)}")

# Example usage:
# git_info = await get_git_info()
# if git_info:
#     print(git_info) # main/2021.08.12.1234/1234567890abcdef or Error: <error message>