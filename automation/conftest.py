import pytest

from clients.saleor_client import SaleorClient


@pytest.fixture
def saleor_client():
    return SaleorClient()