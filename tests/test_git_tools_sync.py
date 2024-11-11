import unittest
from unittest.mock import patch, MagicMock
from useful_tools.git_tools_sync import get_last_commit_datetime, get_current_branch, run_git_command, get_commit_id, get_git_info
import subprocess

class TestGitToolsSync(unittest.TestCase):

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_get_last_commit_datetime(self, mock_check_output):
        # Mock the output of the git command
        mock_check_output.return_value = b'2024.11.02.230203\n'
        
        # Call the function
        result = get_last_commit_datetime()
        
        # Verify the result
        self.assertEqual(result, '2024.11.02.230203')
        mock_check_output.assert_called_once_with(["git", "log", "-1", "--date=format:%Y.%m.%d.%H%M", "--format=%cd"], stderr=subprocess.STDOUT)

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_get_current_branch(self, mock_check_output):
        # Mock the output of the git command
        mock_check_output.return_value = b'main\n'
        
        # Call the function
        result = get_current_branch()
        
        # Verify the result
        self.assertEqual(result, 'main')
        mock_check_output.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.STDOUT)

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_run_git_command_success(self, mock_check_output):
        # Mock the output of the git command
        mock_check_output.return_value = b"On branch dev\nYour branch is up to date with 'origin/dev'.\n\nnothing to commit, working tree clean\n"
        
        # Call the function
        result = run_git_command(["git", "status"])
        
        # Verify the result
        self.assertEqual(result, "On branch dev\nYour branch is up to date with 'origin/dev'.\n\nnothing to commit, working tree clean")
        mock_check_output.assert_called_once_with(["git", "status"], stderr=subprocess.STDOUT)

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_run_git_command_dubious_ownership(self, mock_check_output):
        # Mock the output of the git command to simulate dubious ownership error
        mock_check_output.side_effect = [
            subprocess.CalledProcessError(128, 'git', b"fatal: detected dubious ownership in repository at 'C:/code/my-codebase'\n'C:/code/my-codebase' is owned by:\nAzureAD/UserThatOwnsDir (S-1-12-x-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxx-xxxx)\nbut the current user is:\nCOMPUTERNAME/UserScriptIsRunningAs (S-1-5-x-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxx-xxxx)\nTo add an exception for this directory, call:\n\ngit config --global --add safe.directory C:/code/my-codebase\n"), # output for the first call
            b"", # output for the cell to git config
            b"On branch dev\nYour branch is up to date with 'origin/dev'.\n\nnothing to commit, working tree clean\n" # finally, output from the first command run again after adding the directory to the safe list
        ]
        
        # Call the function
        result = run_git_command(["git", "status"])
        
        # Verify the result
        self.assertEqual(result, "On branch dev\nYour branch is up to date with 'origin/dev'.\n\nnothing to commit, working tree clean")
        self.assertEqual(mock_check_output.call_count, 3)
        mock_check_output.assert_any_call(["git", "status"], stderr=subprocess.STDOUT)
        mock_check_output.assert_any_call(["git", "config", "--global", "--add", "safe.directory", "C:/code/my-codebase"])
        mock_check_output.assert_any_call(["git", "status"], stderr=subprocess.STDOUT)

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_run_git_command_error(self, mock_check_output):
        # Mock the output of the git command to simulate a generic error
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'git', b'error\n')
        
        # Call the function and verify that it raises an error
        with self.assertRaises(subprocess.CalledProcessError):
            run_git_command(["git", "status"])

    @patch('useful_tools.git_tools_sync.subprocess.check_output')
    def test_get_commit_id(self, mock_check_output):
        # Mock the output of the git command
        mock_check_output.return_value = b'abcdef123456\n'
        
        # Call the function
        result = get_commit_id()
        
        # Verify the result
        self.assertEqual(result, 'abcdef123456')
        mock_check_output.assert_called_once_with(["git", "rev-parse", "HEAD"], stderr=subprocess.STDOUT)

    @patch('useful_tools.git_tools_sync.get_current_branch')
    @patch('useful_tools.git_tools_sync.get_last_commit_datetime')
    @patch('useful_tools.git_tools_sync.get_commit_id')
    def test_get_git_info(self, mock_get_commit_id, mock_get_last_commit_datetime, mock_get_current_branch):
        # Mock the output of the git commands
        mock_get_current_branch.return_value = 'main'
        mock_get_last_commit_datetime.return_value = '2024.11.02.230203'
        mock_get_commit_id.return_value = 'abcdef123456'
        
        # Call the function
        result = get_git_info()
        
        # Verify the result
        self.assertEqual(result, 'main/2024.11.02.230203/abcdef123456')
        mock_get_current_branch.assert_called_once()
        mock_get_last_commit_datetime.assert_called_once()
        mock_get_commit_id.assert_called_once()

    def test_running_sync_function_in_async_context(self):
        import asyncio
        with self.assertRaises(RuntimeError):
            async def wrapper():
                get_last_commit_datetime()

            asyncio.run(wrapper())

if __name__ == '__main__':
    unittest.main()
