from unittest.mock import patch, MagicMock
from app.monitor import check_json_endpoint

@patch("requests.get")
def test_check_json_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"slideshow": {"title": "Sample"}}
    mock_get.return_value = mock_resp

    result = check_json_endpoint("http://mock-api/test", expected_key="slideshow")
    assert result is True

@patch("requests.get")
def test_check_json_key_mismatch(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"unrelated_key": "data"}
    mock_get.return_value = mock_resp

    result = check_json_endpoint("http://mock-api/test", expected_key="slideshow")
    assert result is False