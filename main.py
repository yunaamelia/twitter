"""
Main entry point for Twitter Giveaway Bot
"""
import logging
import schedule
import time
import sys
from bot import TwitterGiveawayBot
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the bot"""
    logger.info("🚀 Starting Twitter Giveaway Bot")
    logger.info(f"Configuration:")
    logger.info(f"  - Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
    logger.info(f"  - Min token price: ${Config.MIN_TOKEN_PRICE_USD}")
    logger.info(f"  - Min giveaway value: ${Config.MIN_GIVEAWAY_VALUE_USD}")
    logger.info(f"  - Max accounts to use: {Config.MAX_ACCOUNTS_TO_USE}")
    
    try:
        # Initialize bot
        bot = TwitterGiveawayBot()
        
        # Print initial statistics
        stats = bot.get_statistics()
        logger.info("📊 Initial Statistics:")
        for key, value in stats.items():
            logger.info(f"  - {key}: {value}")
        
        # Run first cycle immediately
        logger.info("Running initial cycle...")
        bot.run_cycle()
        
        # Schedule periodic checks
        schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(bot.run_cycle)
        
        logger.info(f"✅ Bot is now running! Checking every {Config.CHECK_INTERVAL_MINUTES} minutes.")
        logger.info("Press Ctrl+C to stop.")
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
