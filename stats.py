"""
Utility script to check bot status and statistics
"""
import sys
from models import SessionLocal, Giveaway, Account, WinnerNotification, init_db
from datetime import datetime, timedelta


def print_statistics():
    """Print comprehensive bot statistics"""
    init_db()
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("Twitter Giveaway Bot - Statistics Dashboard")
        print("=" * 60)
        print()
        
        # Giveaway statistics
        total_giveaways = db.query(Giveaway).count()
        participated = db.query(Giveaway).filter_by(participated=True).count()
        wins = db.query(Giveaway).filter_by(won=True).count()
        
        print("📊 Giveaway Statistics:")
        print(f"  Total giveaways found: {total_giveaways}")
        print(f"  Participated: {participated}")
        print(f"  Wins: {wins}")
        if participated > 0:
            print(f"  Win rate: {(wins/participated*100):.2f}%")
        print()
        
        # Account statistics
        total_accounts = db.query(Account).count()
        active_accounts = db.query(Account).filter_by(is_active=True).count()
        
        print("👥 Account Statistics:")
        print(f"  Total accounts: {total_accounts}")
        print(f"  Active accounts: {active_accounts}")
        print()
        
        # Top performing accounts
        print("🏆 Top Performing Accounts:")
        top_accounts = db.query(Account).order_by(
            Account.total_wins.desc()
        ).limit(5).all()
        
        for i, acc in enumerate(top_accounts, 1):
            print(f"  {i}. @{acc.username or 'Unknown'}: {acc.total_wins} wins, {acc.total_participations} participations")
        print()
        
        # Recent activity
        print("📅 Recent Activity (Last 7 Days):")
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_giveaways = db.query(Giveaway).filter(
            Giveaway.created_at >= week_ago
        ).count()
        
        recent_participations = db.query(Giveaway).filter(
            Giveaway.created_at >= week_ago,
            Giveaway.participated == True
        ).count()
        
        recent_wins = db.query(WinnerNotification).filter(
            WinnerNotification.received_at >= week_ago
        ).count()
        
        print(f"  New giveaways found: {recent_giveaways}")
        print(f"  Participations: {recent_participations}")
        print(f"  Wins: {recent_wins}")
        print()
        
        # Recent wins
        if recent_wins > 0:
            print("🎉 Recent Wins:")
            recent_win_notifications = db.query(WinnerNotification).filter(
                WinnerNotification.received_at >= week_ago
            ).order_by(WinnerNotification.received_at.desc()).all()
            
            for notif in recent_win_notifications[:5]:
                account = db.query(Account).filter_by(
                    account_number=notif.account_number
                ).first()
                username = account.username if account else "Unknown"
                print(f"  - @{username} on {notif.received_at.strftime('%Y-%m-%d %H:%M')}")
            print()
        
        # Token statistics
        print("💰 Token Statistics:")
        tokens = db.query(
            Giveaway.token_symbol,
            Giveaway.token_price_usd
        ).filter(
            Giveaway.token_symbol.isnot(None)
        ).distinct().all()
        
        print(f"  Unique tokens tracked: {len(tokens)}")
        if tokens:
            print("  Top tokens:")
            for token, price in list(tokens)[:10]:
                if price:
                    print(f"    - {token}: ${price:.4f}")
        
        print()
        print("=" * 60)
        
    finally:
        db.close()


if __name__ == "__main__":
    print_statistics()
