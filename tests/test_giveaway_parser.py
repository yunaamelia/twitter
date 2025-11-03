"""
Tests for giveaway parser module
"""
import pytest

from giveaway_parser import GiveawayParser


@pytest.fixture
def parser():
    """Create a parser instance"""
    return GiveawayParser()


def test_is_giveaway_tweet(parser):
    """Test giveaway detection"""
    # Should detect giveaway
    assert parser.is_giveaway_tweet("Win 100 BTC! Crypto giveaway!")
    assert parser.is_giveaway_tweet("Free ETH airdrop for everyone")
    assert parser.is_giveaway_tweet("Token giveaway contest")
    
    # Should not detect as giveaway
    assert not parser.is_giveaway_tweet("Just bought some BTC")
    assert not parser.is_giveaway_tweet("Random tweet about nothing")


def test_parse_rules_follow(parser):
    """Test follow rule parsing"""
    rules = parser.parse_rules("Follow @user and RT to win!")
    assert rules['follow'] is True
    
    rules = parser.parse_rules("Must follow us to participate")
    assert rules['follow'] is True


def test_parse_rules_retweet(parser):
    """Test retweet rule parsing"""
    rules = parser.parse_rules("Retweet this post to enter")
    assert rules['retweet'] is True
    
    rules = parser.parse_rules("RT and win!")
    assert rules['retweet'] is True


def test_parse_rules_like(parser):
    """Test like rule parsing"""
    rules = parser.parse_rules("Like this tweet to participate")
    assert rules['like'] is True
    
    rules = parser.parse_rules("❤️ to enter")
    assert rules['like'] is True


def test_parse_rules_comment(parser):
    """Test comment rule parsing"""
    rules = parser.parse_rules("Comment your wallet address")
    assert rules['comment'] is True
    
    rules = parser.parse_rules("Reply with 💬 to win")
    assert rules['comment'] is True


def test_parse_rules_multiple(parser):
    """Test parsing multiple rules"""
    text = """
    🎁 GIVEAWAY 🎁
    Win 100 $TOKEN!
    ✅ Follow @Organizer
    ✅ Retweet
    ✅ Like
    ✅ Comment your wallet
    """
    rules = parser.parse_rules(text)
    assert rules['follow'] is True
    assert rules['retweet'] is True
    assert rules['like'] is True
    assert rules['comment'] is True


def test_generate_comment(parser):
    """Test comment generation"""
    comment = parser.generate_comment("Win BTC!")
    assert isinstance(comment, str)
    assert len(comment) > 0
    
    # Should generate different comments
    comments = [parser.generate_comment("test") for _ in range(10)]
    assert len(set(comments)) > 1  # At least some variety


def test_extract_mentioned_accounts(parser):
    """Test extracting @mentions"""
    text = "Follow @user1 and @user2 to win!"
    mentions = parser.extract_mentioned_accounts(text)
    assert 'user1' in mentions
    assert 'user2' in mentions
    assert len(mentions) == 2
