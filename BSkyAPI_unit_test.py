import unittest
from unittest.mock import patch, Mock
import json
from datetime import datetime
import os
import pandas as pd
from BSkyAPI import BlueskyAPI

class TestBlueskyAPI(unittest.TestCase):
    @patch("requests.get")
    def test_get_posts_from_search(self, mock_get):
        """Test the 'get_posts_from_search' method."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "posts": [
                {
                    "author": {"displayName": "User1"},
                    "record": {"createdAt": "2025-05-08T00:00:00Z", "text": "Hello World"}
                },
                {
                    "author": {"displayName": "User2"},
                    "record": {"createdAt": "2025-05-08T01:00:00Z", "text": "Test Post"}
                }
            ]
        }
        mock_get.return_value = mock_response

        # Test the method
        api = BlueskyAPI()
        result_df = api.get_posts_from_search("test", "latest", "en")
        
        # Validate the result
        self.assertEqual(result_df.shape[0], 2)
        self.assertEqual(result_df.columns.tolist(), ['display_name', 'created_at', 'text'])
        self.assertEqual(result_df.iloc[0]['display_name'], 'User1')
        self.assertEqual(result_df.iloc[1]['text'], 'Test Post')

    @patch("requests.get")
    def test_get_posts_from_handle(self, mock_get):
        """Test the 'get_posts_from_handle' method."""
        # Setup mock response for get_posts_from_handle
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "feed": [
                {
                    "post": {
                        "record": {
                            "createdAt": "2025-05-08T00:00:00Z",
                            "text": "Post by User1"
                        }
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # Test the method
        api = BlueskyAPI()
        result_df = api.get_posts_from_handle("user_handle")

        # Validate the result
        self.assertEqual(result_df.shape[0], 1)
        self.assertEqual(result_df.columns.tolist(), ['created_at', 'text'])
        self.assertEqual(result_df.iloc[0]['text'], 'Post by User1')

    @patch("requests.get")
    def test_handle_validation_existing_handle(self, mock_get):
        """Test handle validation for an existing handle."""
        # Mock a successful response for handle validation
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test the method with a valid handle
        api = BlueskyAPI()
        result = api.handle_validation("user_handle")
        self.assertTrue(result)

    @patch("requests.get")
    def test_handle_validation_non_existing_handle(self, mock_get):
        """Test handle validation for a non-existing handle."""
        # Mock a 404 error response for handle validation (handle not found)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test the method with an invalid handle
        api = BlueskyAPI()
        result = api.handle_validation("invalid_handle")
        self.assertFalse(result)



