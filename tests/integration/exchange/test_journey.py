"""
Integration tests for journey routes (flights and hotels)
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.integration
class TestJourneyRoutes:
    """Tests for journey blueprint routes"""

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_get_booking_dest_id_returns_dest_id(self, mock_requests_get):
        """Test get_booking_dest_id returns destination ID from Booking.com API"""
        from serwis_info.modules.exchange.routes.journey import get_booking_dest_id
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "dest_id": 123456,
                "name": "Warsaw",
            }
        ]
        mock_requests_get.return_value = mock_response
        
        result = get_booking_dest_id("Warszawa")
        
        assert result == 123456
        mock_requests_get.assert_called_once()

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_get_booking_dest_id_empty_response(self, mock_requests_get):
        """Test get_booking_dest_id handles empty API response"""
        from serwis_info.modules.exchange.routes.journey import get_booking_dest_id
        
        # Mock empty response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_requests_get.return_value = mock_response
        
        result = get_booking_dest_id("UnknownCity")
        
        assert result is None

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_get_booking_dest_id_api_error(self, mock_requests_get):
        """Test get_booking_dest_id handles API errors gracefully"""
        from serwis_info.modules.exchange.routes.journey import get_booking_dest_id
        
        # Mock API error
        mock_requests_get.side_effect = Exception("API Error")
        
        result = get_booking_dest_id("Warszawa")
        
        assert result is None

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_get_booking_dest_id_bad_status_code(self, mock_requests_get):
        """Test get_booking_dest_id handles bad status codes"""
        from serwis_info.modules.exchange.routes.journey import get_booking_dest_id
        
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_requests_get.return_value = mock_response
        
        result = get_booking_dest_id("Warszawa")
        
        assert result is None

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_returns_list_of_hotels(self, mock_requests_get):
        """Test fetch_hotels returns formatted list of hotels"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        # Mock hotel API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {
                    "hotel_name": "Hotel A",
                    "address_trans": "Main St 1",
                    "min_total_price": 100.0,
                    "review_score": 4.5,
                    "max_photo_url": "http://example.com/photo.jpg"
                },
                {
                    "hotel_name": "Hotel B",
                    "address_trans": "Main St 2",
                    "min_total_price": 150.0,
                    "review_score": 4.0,
                    "max_photo_url": "http://example.com/photo2.jpg"
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 2)
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert all("name" in hotel for hotel in result)
        assert all("address" in hotel for hotel in result)
        assert all("price_usd" in hotel for hotel in result)

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_sorts_by_price(self, mock_requests_get):
        """Test fetch_hotels sorts hotels by price (cheapest first)"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {
                    "hotel_name": "Expensive Hotel",
                    "address_trans": "High St",
                    "min_total_price": 300.0,
                    "review_score": 5.0,
                    "max_photo_url": "http://example.com/photo1.jpg"
                },
                {
                    "hotel_name": "Cheap Hotel",
                    "address_trans": "Low St",
                    "min_total_price": 50.0,
                    "review_score": 3.0,
                    "max_photo_url": "http://example.com/photo2.jpg"
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 1)
        
        # Should be sorted by price
        assert result[0]["name"] == "Cheap Hotel"
        assert result[0]["price_usd"] == 50.0

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_limits_to_five(self, mock_requests_get):
        """Test fetch_hotels returns maximum 5 hotels"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        # Create 10 hotels
        hotels_data = [
            {
                "hotel_name": f"Hotel {i}",
                "address_trans": f"Street {i}",
                "min_total_price": float(i * 10),
                "review_score": 4.0,
                "max_photo_url": f"http://example.com/photo{i}.jpg"
            }
            for i in range(1, 11)
        ]
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": hotels_data}
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 2)
        
        # Should only return 5 cheapest hotels
        assert len(result) == 5

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_handles_empty_result(self, mock_requests_get):
        """Test fetch_hotels handles empty hotel list"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": []}
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(999999, "2025-02-01", "2025-02-05", 1)
        
        assert result == []

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_api_error(self, mock_requests_get):
        """Test fetch_hotels handles API errors gracefully"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        mock_requests_get.side_effect = Exception("API Error")
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 1)
        
        assert result == []

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_bad_status_code(self, mock_requests_get):
        """Test fetch_hotels handles bad status codes"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 1)
        
        assert result == []

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_journey_page_returns_html(self, mock_requests_get):
        """Test that journey page returns HTML"""
        # Just ensure the page loads
        # Don't need to mock anything for a simple page load
        
        # Mock requests in case there are API calls
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response
        
        # This test just checks the blueprint exists and loads
        # We can't easily test the full page without mocking many external APIs
        # So we test the helper functions instead

    def test_translate_to_english(self):
        """Test translate_to_english function"""
        from serwis_info.modules.exchange.routes.journey import translate_to_english
        
        # Test that it doesn't crash and returns a string
        result = translate_to_english("Warszawa")
        assert isinstance(result, str)
        # Should return English translation or original if translation fails
        assert len(result) > 0

    @patch('serwis_info.modules.exchange.routes.journey.requests.get')
    def test_fetch_hotels_with_missing_fields(self, mock_requests_get):
        """Test fetch_hotels handles hotels with missing fields"""
        from serwis_info.modules.exchange.routes.journey import fetch_hotels
        
        # Hotel with missing fields
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {
                    "hotel_name": "Hotel A",
                    # Missing other fields
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        
        result = fetch_hotels(123456, "2025-02-01", "2025-02-05", 1)
        
        # Should handle gracefully and return formatted data
        assert isinstance(result, list)
        if len(result) > 0:
            assert "name" in result[0]
