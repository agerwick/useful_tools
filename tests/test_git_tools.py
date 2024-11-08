import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from useful_tools.git_tools import get_git_info, get_last_commit_datetime, get_current_branch, get_commit_id

class TestGitToolsSync(unittest.TestCase):

    @patch('useful_tools.git_tools.sync_get_git_info')
    @patch('useful_tools.git_tools.async_get_git_info', new_callable=AsyncMock)
    def test_get_git_info_sync(self, mock_async_get_git_info, mock_sync_get_git_info):
        # Mock the synchronous function
        mock_sync_get_git_info.return_value = 'sync_git_info'

        # Test in synchronous context
        result = get_git_info()
        self.assertEqual(result, 'sync_git_info')
        mock_sync_get_git_info.assert_called_once()
        mock_async_get_git_info.assert_not_called()

    @patch('useful_tools.git_tools.sync_get_last_commit_datetime')
    @patch('useful_tools.git_tools.async_get_last_commit_datetime', new_callable=AsyncMock)
    def test_get_last_commit_datetime_sync(self, mock_async_get_last_commit_datetime, mock_sync_get_last_commit_datetime):
        # Mock the synchronous function
        mock_sync_get_last_commit_datetime.return_value = 'sync_commit_datetime'
        
        # Test in synchronous context
        result = get_last_commit_datetime()
        self.assertEqual(result, 'sync_commit_datetime')
        mock_sync_get_last_commit_datetime.assert_called_once()
        mock_async_get_last_commit_datetime.assert_not_called()

    @patch('useful_tools.git_tools.sync_get_current_branch')
    @patch('useful_tools.git_tools.async_get_current_branch', new_callable=AsyncMock)
    def test_get_current_branch_sync(self, mock_async_get_current_branch, mock_sync_get_current_branch):
        # Mock the synchronous function
        mock_sync_get_current_branch.return_value = 'sync_branch'
        
        # Test in synchronous context
        result = get_current_branch()
        self.assertEqual(result, 'sync_branch')
        mock_sync_get_current_branch.assert_called_once()
        mock_async_get_current_branch.assert_not_called()

    @patch('useful_tools.git_tools.sync_get_commit_id')
    @patch('useful_tools.git_tools.async_get_commit_id', new_callable=AsyncMock)
    def test_get_commit_id_sync(self, mock_async_get_commit_id, mock_sync_get_commit_id):
        # Mock the synchronous function
        mock_sync_get_commit_id.return_value = 'sync_commit_id'
        
        # Test in synchronous context
        result = get_commit_id()
        self.assertEqual(result, 'sync_commit_id')
        mock_sync_get_commit_id.assert_called_once()
        mock_async_get_commit_id.assert_not_called()



class TestGitToolsAsync(unittest.TestCase):

    @patch('useful_tools.git_tools.sync_get_git_info')
    @patch('useful_tools.git_tools.async_get_git_info', new_callable=AsyncMock)
    def test_get_git_info_async(self, mock_async_get_git_info, mock_sync_get_git_info):
        # Mock the asynchronous function
        mock_async_get_git_info.return_value = 'async_git_info'
        
        async def test_async():
            result = await get_git_info()
            self.assertEqual(result, 'async_git_info')
            mock_async_get_git_info.assert_called_once()
            mock_sync_get_git_info.assert_not_called()
        
        asyncio.run(test_async())

    @patch('useful_tools.git_tools.sync_get_last_commit_datetime')
    @patch('useful_tools.git_tools.async_get_last_commit_datetime', new_callable=AsyncMock)
    def test_get_last_commit_datetime_async(self, mock_async_get_last_commit_datetime, mock_sync_get_last_commit_datetime):
        # Mock the asynchronous function
        mock_async_get_last_commit_datetime.return_value = 'async_commit_datetime'
        
        async def test_async():
            result = await get_last_commit_datetime()
            self.assertEqual(result, 'async_commit_datetime')
            mock_async_get_last_commit_datetime.assert_called_once()
            mock_sync_get_last_commit_datetime.assert_not_called()
        
        asyncio.run(test_async())

    @patch('useful_tools.git_tools.sync_get_current_branch')
    @patch('useful_tools.git_tools.async_get_current_branch', new_callable=AsyncMock)
    def test_get_current_branch_async(self, mock_async_get_current_branch, mock_sync_get_current_branch):
        # Mock the asynchronous function
        mock_async_get_current_branch.return_value = 'async_branch'
        
        async def test_async():
            result = await get_current_branch()
            self.assertEqual(result, 'async_branch')
            mock_async_get_current_branch.assert_called_once()
            mock_sync_get_current_branch.assert_not_called()
        
        asyncio.run(test_async())

    @patch('useful_tools.git_tools.sync_get_commit_id')
    @patch('useful_tools.git_tools.async_get_commit_id', new_callable=AsyncMock)
    def test_get_commit_id_async(self, mock_async_get_commit_id, mock_sync_get_commit_id):
        # Mock the asynchronous function
        mock_async_get_commit_id.return_value = 'async_commit_id'
        
        async def test_async():
            result = await get_commit_id()
            self.assertEqual(result, 'async_commit_id')
            mock_async_get_commit_id.assert_called_once()
            mock_sync_get_commit_id.assert_not_called()
        
        asyncio.run(test_async())

if __name__ == '__main__':
    unittest.main()
