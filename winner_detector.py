"""
Winner detection system for monitoring DMs and mentions
"""
import tweepy
from typing import List, Dict, Optional
from models import WinnerNotification, Giveaway, SessionLocal
from account_manager import TwitterAccountManager
from datetime import datetime, timedelta
import logging
import re

logger = logging.getLogger(__name__)


class WinnerDetector:
    """Detect winner announcements via DMs and mentions"""
    
    def __init__(self, account_manager: TwitterAccountManager):
        self.account_manager = account_manager
    
    def check_for_winners(self):
        """Check all accounts for winner notifications"""
        logger.info("Checking for winner notifications...")
        
        for account_num in self.account_manager.get_active_accounts():
            try:
                # Check DMs
                self._check_dms(account_num)
                
                # Check mentions
                self._check_mentions(account_num)
                
            except Exception as e:
                logger.error(f"Error checking account {account_num} for winners: {e}")
    
    def _check_dms(self, account_number: int):
        """
        Check DMs for winner notifications
        
        Note: Requires Twitter API v2 with DM read permissions
        """
        try:
            client = self.account_manager.get_account(account_number)
            if not client:
                return
            
            # Get recent DMs (last 24 hours)
            # Note: This requires special permissions from Twitter
            # For now, we'll log that DM checking is not fully implemented
            logger.debug(f"DM checking for account {account_number} (requires elevated API access)")
            
            # Placeholder for DM checking logic
            # When API access is available, implement:
            # 1. Get DMs from last 24 hours
            # 2. Search for winner-related keywords
            # 3. Save notifications to database
            
        except Exception as e:
            logger.error(f"Error checking DMs for account {account_number}: {e}")
    
    def _check_mentions(self, account_number: int):
        """Check mentions for winner announcements"""
        try:
            client = self.account_manager.get_account(account_number)
            if not client:
                return
            
            account_info = self.account_manager.account_info.get(account_number)
            if not account_info:
                return
            
            user_id = account_info['id']
            
            # Get mentions from last 24 hours
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=24)
            
            mentions = client.get_users_mentions(
                id=user_id,
                start_time=start_time.isoformat() + 'Z',
                end_time=end_time.isoformat() + 'Z',
                max_results=100,
                tweet_fields=['created_at', 'author_id', 'text']
            )
            
            if not mentions.data:
                return
            
            for tweet in mentions.data:
                # Check if mention looks like a winner announcement
                if self._is_winner_announcement(tweet.text):
                    self._save_winner_notification(
                        account_number=account_number,
                        notification_type='mention',
                        notification_text=tweet.text,
                        tweet_id=tweet.id,
                        author_id=tweet.author_id
                    )
                    logger.info(f"🎉 Winner notification detected for account {account_number}!")
            
        except Exception as e:
            logger.error(f"Error checking mentions for account {account_number}: {e}")
    
    def _is_winner_announcement(self, text: str) -> bool:
        """Check if text is a winner announcement"""
        text_lower = text.lower()
        
        winner_keywords = [
            'congratulations',
            'congrats',
            'winner',
            'won',
            'you win',
            'you won',
            'claim your prize',
            'you\'re the winner',
            'selected winner',
            'you have been selected',
        ]
        
        return any(keyword in text_lower for keyword in winner_keywords)
    
    def _save_winner_notification(self, account_number: int, notification_type: str, 
                                   notification_text: str, tweet_id: str = None, 
                                   author_id: str = None):
        """Save winner notification to database"""
        db = SessionLocal()
        try:
            # Check if notification already exists
            existing = db.query(WinnerNotification).filter_by(
                account_number=account_number,
                notification_text=notification_text
            ).first()
            
            if existing:
                return
            
            # Find related giveaway if possible
            giveaway_id = None
            if author_id:
                giveaway = db.query(Giveaway).filter_by(
                    author_id=author_id,
                    participated=True
                ).order_by(Giveaway.created_at.desc()).first()
                
                if giveaway:
                    giveaway_id = giveaway.id
                    giveaway.won = True
                    giveaway.winner_announced = True
            
            # Save notification
            notification = WinnerNotification(
                giveaway_id=giveaway_id,
                account_number=account_number,
                notification_type=notification_type,
                notification_text=notification_text
            )
            db.add(notification)
            db.commit()
            
            # Update account stats
            self.account_manager.update_account_stats(account_number, won=True)
            
            logger.info(f"Winner notification saved for account {account_number}")
            
        finally:
            db.close()
    
    def get_recent_wins(self, days: int = 7) -> List[Dict]:
        """Get recent wins from all accounts"""
        db = SessionLocal()
        try:
            cutoff = datetime.utcnow() - timedelta(days=days)
            
            notifications = db.query(WinnerNotification).filter(
                WinnerNotification.received_at >= cutoff
            ).order_by(WinnerNotification.received_at.desc()).all()
            
            results = []
            for notif in notifications:
                results.append({
                    'account_number': notif.account_number,
                    'type': notif.notification_type,
                    'text': notif.notification_text,
                    'received_at': notif.received_at,
                    'giveaway_id': notif.giveaway_id
                })
            
            return results
            
        finally:
            db.close()
