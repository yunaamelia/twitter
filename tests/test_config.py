"""
Tests for configuration module
"""
import pytest

from config import Config


def test_config_has_default_values():
    """Test that config has sensible defaults"""
    assert Config.MIN_TOKEN_PRICE_USD >= 0
    assert Config.MAX_ACCOUNTS_TO_USE > 0
    assert Config.CHECK_INTERVAL_MINUTES > 0
    assert Config.MIN_FOLLOWERS_REQUIRED >= 0
    assert Config.MIN_GIVEAWAY_VALUE_USD >= 0


def test_config_keywords():
    """Test that config has necessary keywords"""
    assert len(Config.CRYPTO_KEYWORDS) > 0
    assert len(Config.TOKEN_KEYWORDS) > 0
    assert len(Config.ACTION_KEYWORDS) > 0
    
    assert 'follow' in Config.ACTION_KEYWORDS
    assert 'retweet' in Config.ACTION_KEYWORDS
    assert 'like' in Config.ACTION_KEYWORDS
    assert 'comment' in Config.ACTION_KEYWORDS


def test_get_account_credentials():
    """Test account credentials retrieval"""
    creds = Config.get_account_credentials(1)
    assert isinstance(creds, dict)
    assert 'api_key' in creds
    assert 'api_secret' in creds
    assert 'access_token' in creds
    assert 'access_secret' in creds
