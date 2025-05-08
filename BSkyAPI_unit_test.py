import unittest
from unittest.mock import patch, Mock
import json
from datetime import datetime
import os
import pandas as pd

from BSkyAPI import BlueskyAPI  # Assuming the class is in bluesky_api.py


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

    @patch("requests.get")
    def test_create_csv(self, mock_get):
        """Test the 'create_csv' method."""
        # Prepare some test posts data
        posts = [
            {"display_name": "User1", "created_at": "2025-05-08T00:00:00Z", "text": "Hello World"},
            {"display_name": "User2", "created_at": "2025-05-08T01:00:00Z", "text": "Test Post"}
        ]
        
        # Mock file I/O by using StringIO instead of actual file creation
        from io import StringIO
        import csv

        # Create a temporary "file"
        temp_file = StringIO()
        writer = csv.DictWriter(temp_file, fieldnames=["display_name", "created_at", "text"])
        writer.writeheader()
        writer.writerows(posts)
        
        # Test create_csv method
        api = BlueskyAPI()
        api.create_csv(posts)

        # Check if the file was created successfully
        # This part could be further expanded with actual file checks, but here we are mocking it.
        self.assertTrue(os.path.exists("post_data.csv"))

        # Read the file to ensure content
        df = pd.read_csv("post_data.csv")
        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.columns.tolist(), ['display_name', 'created_at', 'text'])

    @patch("requests.get")
    def test_create_csv_filtered(self, mock_get):
        """Test filtered CSV creation for empty text fields."""
        # Prepare some test posts data
        posts = [
            {"display_name": "User1", "created_at": "2025-05-08T00:00:00Z", "text": "Hello World"},
            {"display_name": "User2", "created_at": "2025-05-08T01:00:00Z", "text": "Test Post"},
            {"display_name": "User3", "created_at": "2025-05-08T02:00:00Z", "text": ""}
        ]

        api = BlueskyAPI()
        # Mock file I/O by using StringIO instead of actual file creation
        from io import StringIO
        import csv

        # Mock the CSV creation process
        api.create_csv(posts)

        # Check if the file "post_data_filtered.csv" is created
        df_filtered = pd.read_csv("post_data_filtered.csv")
        self.assertEqual(df_filtered.shape[0], 2)  # One row should be filtered out due to blank text
        self.assertEqual(df_filtered.columns.tolist(), ['display_name', 'created_at', 'text'])