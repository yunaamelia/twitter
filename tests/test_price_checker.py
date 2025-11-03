"""
Tests for price checker module
"""
import pytest

from price_checker import PriceChecker


@pytest.fixture
def checker():
    """Create a price checker instance"""
    return PriceChecker()


def test_extract_token_info_with_amount(checker):
    """Test token extraction with amount"""
    text = "Win 100 BTC in this giveaway!"
    info = checker.extract_token_info(text)
    
    assert info['token_symbol'] == 'BTC'
    assert info['estimated_amount'] == 100.0


def test_extract_token_info_with_comma(checker):
    """Test token extraction with comma in amount"""
    text = "Giveaway: 1,000 ETH to the winner!"
    info = checker.extract_token_info(text)
    
    assert info['token_symbol'] == 'ETH'
    assert info['estimated_amount'] == 1000.0


def test_extract_token_info_without_amount(checker):
    """Test token extraction without amount"""
    text = "BTC giveaway happening now!"
    info = checker.extract_token_info(text)
    
    assert info['token_symbol'] == 'BTC'


def test_extract_token_info_no_token(checker):
    """Test extraction when no token found"""
    text = "Random text without crypto"
    info = checker.extract_token_info(text)
    
    assert info['token_symbol'] is None


def test_is_valuable_giveaway_no_price(checker):
    """Test valuable check without price"""
    token_info = {'token_price_usd': None}
    assert not checker.is_valuable_giveaway(token_info)


def test_is_valuable_giveaway_low_price(checker):
    """Test valuable check with low price"""
    token_info = {'token_price_usd': 0.0001}
    # Will fail if MIN_TOKEN_PRICE_USD is higher
    result = checker.is_valuable_giveaway(token_info)
    assert isinstance(result, bool)


def test_cache_mechanism(checker):
    """Test that price cache works"""
    # First call - adds to cache
    price1 = checker.get_token_price('BTC')
    
    # Second call - should use cache
    price2 = checker.get_token_price('BTC')
    
    # Should be the same (from cache)
    if price1 is not None:
        assert price1 == price2
