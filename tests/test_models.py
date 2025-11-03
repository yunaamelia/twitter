"""
Tests for database models
"""
from datetime import datetime

import pytest

from models import Account, Giveaway, SessionLocal, WinnerNotification, init_db


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    init_db()
    session = SessionLocal()
    yield session
    session.close()


def test_create_giveaway(db_session):
    """Test creating a giveaway"""
    giveaway = Giveaway(
        tweet_id="123456789",
        author_id="987654321",
        author_username="testuser",
        tweet_text="Win 100 BTC!",
        token_symbol="BTC",
        token_price_usd=50000.0
    )
    
    db_session.add(giveaway)
    db_session.commit()
    
    # Retrieve and verify
    saved = db_session.query(Giveaway).filter_by(tweet_id="123456789").first()
    assert saved is not None
    assert saved.author_username == "testuser"
    assert saved.token_symbol == "BTC"
    assert saved.participated is False


def test_create_account(db_session):
    """Test creating an account"""
    account = Account(
        account_number=1,
        username="testbot",
        user_id="111222333"
    )
    
    db_session.add(account)
    db_session.commit()
    
    saved = db_session.query(Account).filter_by(account_number=1).first()
    assert saved is not None
    assert saved.username == "testbot"
    assert saved.is_active is True
    assert saved.total_participations == 0
    assert saved.total_wins == 0


def test_create_winner_notification(db_session):
    """Test creating a winner notification"""
    notification = WinnerNotification(
        giveaway_id=1,
        account_number=1,
        notification_type="mention",
        notification_text="Congratulations! You won!"
    )
    
    db_session.add(notification)
    db_session.commit()
    
    saved = db_session.query(WinnerNotification).filter_by(account_number=1).first()
    assert saved is not None
    assert saved.notification_type == "mention"
    assert saved.processed is False


def test_giveaway_unique_tweet_id(db_session):
    """Test that tweet_id must be unique"""
    giveaway1 = Giveaway(
        tweet_id="duplicate_id",
        author_id="1",
        author_username="user1",
        tweet_text="Test 1"
    )
    db_session.add(giveaway1)
    db_session.commit()
    
    # Try to add duplicate
    giveaway2 = Giveaway(
        tweet_id="duplicate_id",
        author_id="2",
        author_username="user2",
        tweet_text="Test 2"
    )
    db_session.add(giveaway2)
    
    with pytest.raises(Exception):
        db_session.commit()


def test_account_unique_number(db_session):
    """Test that account_number must be unique"""
    account1 = Account(
        account_number=99,
        username="user1"
    )
    db_session.add(account1)
    db_session.commit()
    
    account2 = Account(
        account_number=99,
        username="user2"
    )
    db_session.add(account2)
    
    with pytest.raises(Exception):
        db_session.commit()
