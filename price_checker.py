"""
Price checker for cryptocurrency tokens
"""
import requests
from typing import Optional, Dict
from pycoingecko import CoinGeckoAPI
from config import Config
import logging
import re

logger = logging.getLogger(__name__)


class PriceChecker:
    """Check cryptocurrency prices"""
    
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.cache = {}  # Simple price cache
        
    def get_token_price(self, token_symbol: str) -> Optional[float]:
        """
        Get token price in USD
        
        Args:
            token_symbol: Token symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            Price in USD or None if not found
        """
        token_symbol = token_symbol.upper().strip()
        
        # Check cache first
        if token_symbol in self.cache:
            return self.cache[token_symbol]
        
        try:
            # Try CoinGecko API
            price = self._get_price_from_coingecko(token_symbol)
            if price:
                self.cache[token_symbol] = price
                return price
                
        except Exception as e:
            logger.error(f"Error getting price for {token_symbol}: {e}")
        
        return None
    
    def _get_price_from_coingecko(self, token_symbol: str) -> Optional[float]:
        """Get price from CoinGecko API"""
        try:
            # Map common symbols to CoinGecko IDs
            symbol_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'BNB': 'binancecoin',
                'SOL': 'solana',
                'ADA': 'cardano',
                'XRP': 'ripple',
                'DOGE': 'dogecoin',
                'USDT': 'tether',
                'USDC': 'usd-coin',
                'MATIC': 'matic-network',
                'DOT': 'polkadot',
                'AVAX': 'avalanche-2',
                'LINK': 'chainlink',
                'UNI': 'uniswap',
                'ATOM': 'cosmos',
            }
            
            coin_id = symbol_map.get(token_symbol)
            
            if not coin_id:
                # Try to find by symbol
                coins_list = self.cg.get_coins_list()
                for coin in coins_list:
                    if coin.get('symbol', '').upper() == token_symbol:
                        coin_id = coin['id']
                        break
            
            if coin_id:
                data = self.cg.get_price(ids=coin_id, vs_currencies='usd')
                if coin_id in data and 'usd' in data[coin_id]:
                    return float(data[coin_id]['usd'])
                    
        except Exception as e:
            logger.error(f"CoinGecko API error for {token_symbol}: {e}")
        
        return None
    
    def extract_token_info(self, text: str) -> Dict[str, any]:
        """
        Extract token information from giveaway text
        
        Args:
            text: Giveaway tweet text
            
        Returns:
            Dictionary with token_symbol, token_name, estimated_amount
        """
        text_upper = text.upper()
        
        # Common crypto symbols pattern
        symbol_pattern = r'\b([A-Z]{2,10})\b'
        amount_pattern = r'(\d+(?:,\d+)*(?:\.\d+)?)\s*([A-Z]{2,10})'
        
        tokens_found = []
        
        # Look for amounts with token symbols
        for match in re.finditer(amount_pattern, text_upper):
            amount_str = match.group(1).replace(',', '')
            symbol = match.group(2)
            try:
                amount = float(amount_str)
                tokens_found.append({
                    'symbol': symbol,
                    'amount': amount
                })
            except ValueError:
                pass
        
        # If we found tokens with amounts, return the first one
        if tokens_found:
            token = tokens_found[0]
            price = self.get_token_price(token['symbol'])
            
            return {
                'token_symbol': token['symbol'],
                'token_name': token['symbol'],
                'estimated_amount': token['amount'],
                'token_price_usd': price,
                'estimated_value_usd': token['amount'] * price if price else None
            }
        
        # Otherwise, just look for token symbols
        known_tokens = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA', 'XRP', 'DOGE', 
                       'USDT', 'USDC', 'MATIC', 'DOT', 'AVAX', 'LINK', 
                       'UNI', 'ATOM']
        
        for token in known_tokens:
            if token in text_upper:
                price = self.get_token_price(token)
                return {
                    'token_symbol': token,
                    'token_name': token,
                    'estimated_amount': None,
                    'token_price_usd': price,
                    'estimated_value_usd': None
                }
        
        return {
            'token_symbol': None,
            'token_name': None,
            'estimated_amount': None,
            'token_price_usd': None,
            'estimated_value_usd': None
        }
    
    def is_valuable_giveaway(self, token_info: Dict) -> bool:
        """
        Check if giveaway meets minimum value requirements
        
        Args:
            token_info: Token information dictionary
            
        Returns:
            True if giveaway meets requirements
        """
        # Check if token has a price (i.e., it's a real, traded token)
        if not token_info.get('token_price_usd'):
            return False
        
        # Check minimum price
        if token_info['token_price_usd'] < Config.MIN_TOKEN_PRICE_USD:
            return False
        
        # If we have estimated value, check it
        if token_info.get('estimated_value_usd'):
            if token_info['estimated_value_usd'] < Config.MIN_GIVEAWAY_VALUE_USD:
                return False
        
        return True
