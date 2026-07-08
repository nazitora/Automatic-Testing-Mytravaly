import pytest
import requests

from utils.config import ADMIN_ROUTE_PATHS, BASE_URL


@pytest.mark.regression
@pytest.mark.parametrize("path", ADMIN_ROUTE_PATHS)
def test_admin_login_dashboard_routes_are_not_exposed(path):
    """Document current Render behavior for common admin routes."""
    response = requests.get(f"{BASE_URL}/{path}", timeout=20)

    assert response.status_code == 404
