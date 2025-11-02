"""
Database models for Twitter Giveaway Bot
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Giveaway(Base):
    """Model for storing giveaway information"""
    __tablename__ = 'giveaways'
    
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String(50), unique=True, nullable=False)
    author_id = Column(String(50), nullable=False)
    author_username = Column(String(100), nullable=False)
    tweet_text = Column(Text, nullable=False)
    token_name = Column(String(100))
    token_symbol = Column(String(20))
    token_price_usd = Column(Float)
    estimated_value_usd = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)
    
    # Participation tracking
    participated = Column(Boolean, default=False)
    followed = Column(Boolean, default=False)
    retweeted = Column(Boolean, default=False)
    liked = Column(Boolean, default=False)
    commented = Column(Boolean, default=False)
    
    # Winner tracking
    won = Column(Boolean, default=False)
    winner_announced = Column(Boolean, default=False)
    checked_at = Column(DateTime)


class Account(Base):
    """Model for storing Twitter account information"""
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    account_number = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    user_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime)
    total_participations = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class WinnerNotification(Base):
    """Model for storing winner notifications"""
    __tablename__ = 'winner_notifications'
    
    id = Column(Integer, primary_key=True)
    giveaway_id = Column(Integer)
    account_number = Column(Integer)
    notification_type = Column(String(20))  # 'dm' or 'mention'
    notification_text = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)


# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///giveaways.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
