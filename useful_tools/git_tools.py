import asyncio
from .git_tools_sync  import    get_git_info as sync_get_git_info, \
                                get_last_commit_datetime as sync_get_last_commit_datetime, \
                                get_current_branch as sync_get_current_branch, \
                                get_commit_id as sync_get_commit_id
from .git_tools_async import    get_git_info as async_get_git_info, \
                                get_last_commit_datetime as async_get_last_commit_datetime, \
                                get_current_branch as async_get_current_branch, \
                                get_commit_id as async_get_commit_id

def get_git_info():
    try:
        asyncio.get_running_loop()
        return async_get_git_info()
    except RuntimeError:
        return sync_get_git_info()

def get_last_commit_datetime():
    try:
        asyncio.get_running_loop()
        return async_get_last_commit_datetime()
    except RuntimeError:
        return sync_get_last_commit_datetime()

def get_current_branch():
    try:
        asyncio.get_running_loop()
        return async_get_current_branch()
    except RuntimeError:
        return sync_get_current_branch()
    
def get_commit_id():
    try:
        asyncio.get_running_loop()
        return async_get_commit_id()
    except RuntimeError:
        return sync_get_commit_id()
