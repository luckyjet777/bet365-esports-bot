#!/usr/bin/env python3
"""
Bet365 eSports Scraper - Example Implementation
Educational/Research purposes only

This scraper demonstrates basic web scraping techniques for eSports data.
Supports: e-soccer FIFA, eBasketball, virtual table tennis, CS, virtual tennis
"""

import requests
import time
import json
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging

class Bet365EsportsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_logging()
        self.setup_session()
        
        # eSports categories mapping
        self.esports_categories = {
            'e_soccer_fifa': 'fifa-esoccer',
            'ebasketball': 'virtual-basketball', 
            'virtual_table_tennis': 'table-tennis-virtual',
            'counter_strike': 'counter-strike',
            'virtual_tennis': 'tennis-virtual'
        }
        
    def setup_logging(self):
        """Setup logging for monitoring scraper activity"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bet365_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_session(self):
        """Configure session with anti-detection headers"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def rotate_user_agent(self):
        """Rotate user agent to avoid blocks"""
        self.session.headers.update({'User-Agent': self.ua.random})
        
    def random_delay(self, min_delay=1, max_delay=3):
        """Add random delay between requests"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def scrape_esports_data(self, category='e_soccer_fifa'):
        """
        Scrape eSports data from Bet365
        
        Args:
            category (str): eSports category to scrape
            
        Returns:
            dict: Scraped data with odds and match information
        """
        try:
            self.logger.info(f"Starting scrape for {category}")
            
            # Rotate user agent for anti-detection
            self.rotate_user_agent()
            
            # Simulate realistic browsing behavior
            self.random_delay(2, 4)
            
            # Example URL structure (replace with actual Bet365 URLs)
            base_url = "https://www.bet365.com"
            category_path = self.esports_categories.get(category, 'esports')
            
            # This is a simplified example - actual implementation would need
            # proper URL construction and handling of Bet365's dynamic content
            url = f"{base_url}/sports/{category_path}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract eSports data (simplified example)
            matches_data = self.parse_esports_matches(soup, category)
            
            self.logger.info(f"Successfully scraped {len(matches_data)} matches for {category}")
            return matches_data
            
        except requests.RequestException as e:
            self.logger.error(f"Request error for {category}: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error for {category}: {str(e)}")
            return []
            
    def parse_esports_matches(self, soup, category):
        """
        Parse eSports matches from HTML content
        
        Args:
            soup: BeautifulSoup object
            category (str): eSports category
            
        Returns:
            list: List of parsed match data
        """
        matches = []
        
        # Example parsing logic - this would need to be adapted
        # to Bet365's actual HTML structure
        match_containers = soup.find_all('div', class_='match-container')
        
        for container in match_containers:
            try:
                match_data = {
                    'category': category,
                    'timestamp': time.time(),
                    'team_home': self.safe_extract_text(container, '.team-home'),
                    'team_away': self.safe_extract_text(container, '.team-away'),
                    'odds_home': self.safe_extract_odds(container, '.odds-home'),
                    'odds_draw': self.safe_extract_odds(container, '.odds-draw'),
                    'odds_away': self.safe_extract_odds(container, '.odds-away'),
                    'match_time': self.safe_extract_text(container, '.match-time'),
                    'league': self.safe_extract_text(container, '.league-name')
                }
                
                # Add category-specific data
                if category == 'e_soccer_fifa':
                    match_data.update(self.parse_fifa_specific_data(container))
                elif category == 'ebasketball':
                    match_data.update(self.parse_basketball_specific_data(container))
                elif category == 'virtual_table_tennis':
                    match_data.update(self.parse_table_tennis_specific_data(container))
                elif category == 'counter_strike':
                    match_data.update(self.parse_cs_specific_data(container))
                elif category == 'virtual_tennis':
                    match_data.update(self.parse_tennis_specific_data(container))
                    
                matches.append(match_data)
                
            except Exception as e:
                self.logger.warning(f"Error parsing match container: {str(e)}")
                continue
                
        return matches
        
    def safe_extract_text(self, container, selector):
        """Safely extract text from HTML element"""
        try:
            element = container.select_one(selector)
            return element.get_text(strip=True) if element else None
        except:
            return None
            
    def safe_extract_odds(self, container, selector):
        """Safely extract odds and convert to float"""
        try:
            odds_text = self.safe_extract_text(container, selector)
            return float(odds_text) if odds_text else None
        except:
            return None
            
    def parse_fifa_specific_data(self, container):
        """Parse FIFA e-soccer specific data"""
        return {
            'total_goals_over_under': self.safe_extract_odds(container, '.total-goals'),
            'both_teams_score': self.safe_extract_odds(container, '.both-score'),
            'first_goal': self.safe_extract_text(container, '.first-goal')
        }
        
    def parse_basketball_specific_data(self, container):
        """Parse eBasketball specific data"""
        return {
            'total_points': self.safe_extract_odds(container, '.total-points'),
            'point_spread': self.safe_extract_odds(container, '.point-spread'),
            'quarter_winner': self.safe_extract_text(container, '.quarter-winner')
        }
        
    def parse_table_tennis_specific_data(self, container):
        """Parse virtual table tennis specific data"""
        return {
            'set_betting': self.safe_extract_odds(container, '.set-betting'),
            'total_points': self.safe_extract_odds(container, '.total-points'),
            'handicap': self.safe_extract_odds(container, '.handicap')
        }
        
    def parse_cs_specific_data(self, container):
        """Parse Counter-Strike specific data"""
        return {
            'map_winner': self.safe_extract_text(container, '.map-winner'),
            'total_rounds': self.safe_extract_odds(container, '.total-rounds'),
            'first_map': self.safe_extract_text(container, '.first-map')
        }
        
    def parse_tennis_specific_data(self, container):
        """Parse virtual tennis specific data"""
        return {
            'set_betting': self.safe_extract_odds(container, '.set-betting'),
            'games_handicap': self.safe_extract_odds(container, '.games-handicap'),
            'total_games': self.safe_extract_odds(container, '.total-games')
        }
        
    def scrape_multiple_markets(self, categories=None, real_time=True):
        """
        Scrape multiple eSports markets
        
        Args:
            categories (list): List of categories to scrape
            real_time (bool): Whether to run in real-time mode
            
        Returns:
            dict: Combined data from all categories
        """
        if categories is None:
            categories = list(self.esports_categories.keys())
            
        all_data = {}
        
        for category in categories:
            self.logger.info(f"Scraping {category}...")
            category_data = self.scrape_esports_data(category)
            all_data[category] = category_data
            
            # Add delay between different categories
            self.random_delay(3, 6)
            
        return all_data
        
    def save_data(self, data, filename=None):
        """Save scraped data to JSON file"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"bet365_esports_data_{timestamp}.json"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            
    def run_continuous_scraping(self, interval=300):
        """
        Run continuous scraping with specified interval
        
        Args:
            interval (int): Interval between scrapes in seconds
        """
        self.logger.info("Starting continuous scraping mode...")
        
        while True:
            try:
                # Scrape all eSports categories
                data = self.scrape_multiple_markets()
                
                # Save data with timestamp
                self.save_data(data)
                
                # Log summary
                total_matches = sum(len(matches) for matches in data.values())
                self.logger.info(f"Scraped {total_matches} total matches across all categories")
                
                # Wait for next iteration
                self.logger.info(f"Waiting {interval} seconds until next scrape...")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.logger.info("Continuous scraping stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in continuous scraping: {str(e)}")
                time.sleep(60)  # Wait 1 minute before retrying


def main():
    """Example usage of the Bet365 eSports scraper"""
    scraper = Bet365EsportsScraper()
    
    # Example 1: Scrape single category
    print("Scraping FIFA e-soccer data...")
    fifa_data = scraper.scrape_esports_data('e_soccer_fifa')
    print(f"Found {len(fifa_data)} FIFA matches")
    
    # Example 2: Scrape multiple categories
    print("\nScraping multiple eSports categories...")
    categories = ['e_soccer_fifa', 'ebasketball', 'virtual_table_tennis']
    multi_data = scraper.scrape_multiple_markets(categories)
    
    # Save data
    scraper.save_data(multi_data, 'esports_sample_data.json')
    
    # Example 3: Uncomment to run continuous scraping
    # scraper.run_continuous_scraping(interval=300)  # Every 5 minutes


if __name__ == "__main__":
    main()