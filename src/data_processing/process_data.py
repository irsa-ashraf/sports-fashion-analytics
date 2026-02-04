"""
Data Processing Pipeline
Cleans and transforms raw data into analysis-ready datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataProcessor:
    def __init__(self, raw_data_path='../../data/raw', processed_data_path='../../data/processed'):
        self.raw_path = Path(raw_data_path)
        self.processed_path = Path(processed_data_path)
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def load_tenniscore_sales(self):
        """Load and process tenniscore sales data"""
        df = pd.read_csv(self.raw_path / 'tenniscore_sales.csv')
        
        # Melt demographic columns
        demo_cols = ['gen_z_growth_pct', 'millennial_growth_pct', 'gen_x_growth_pct', 'baby_boomer_growth_pct']
        
        melted = df.melt(
            id_vars=['category', 'item', 'yoy_growth_pct'],
            value_vars=demo_cols,
            var_name='demographic',
            value_name='demo_growth_pct'
        )
        
        # Clean demographic names
        melted['demographic'] = melted['demographic'].str.replace('_growth_pct', '')
        
        # Drop rows with missing values
        melted = melted.dropna()
        
        return melted
    
    def load_market_data(self):
        """Load and process market growth data"""
        sportswear = pd.read_csv(self.raw_path / 'womens_sportswear_market.csv')
        jersey = pd.read_csv(self.raw_path / 'jersey_market.csv')
        
        # Merge on year
        combined = pd.merge(sportswear, jersey, on='year', how='outer')
        
        return combined
    
    def load_trends_data(self):
        """Load Google Trends data"""
        df = pd.read_csv(self.raw_path / 'google_trends.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def load_challengers_impact(self):
        """Load Challengers movie impact data"""
        df = pd.read_csv(self.raw_path / 'challengers_impact.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def create_summary_stats(self):
        """Create summary statistics for the dashboard"""
        
        # Tenniscore sales summary
        tenniscore = self.load_tenniscore_sales()
        top_items = tenniscore.nlargest(5, 'yoy_growth_pct')[['item', 'yoy_growth_pct']]
        
        # Market growth summary
        market = self.load_market_data()
        latest_market = market[market['year'] == 2024].iloc[0]
        projected_2033 = market[market['year'] == 2033].iloc[0]
        
        # Trends summary
        trends = self.load_trends_data()
        peak_tenniscore = trends['tenniscore'].max()
        current_soccer = trends[trends['date'] >= '2026-01-01']['soccer_jersey'].mean()
        
        summary = {
            'tenniscore_peak_growth': top_items.iloc[0]['yoy_growth_pct'],
            'market_2024_billion': latest_market['market_value_billion_usd'],
            'market_2033_billion': projected_2033['market_value_billion_usd'],
            'market_growth_rate': 7.0,
            'tenniscore_search_peak': peak_tenniscore,
            'soccer_jersey_trend_current': current_soccer,
            'challengers_media_value_million': 42.5
        }
        
        return pd.DataFrame([summary])
    
    def process_all(self):
        """Process all datasets and save to processed folder"""
        
        print("Processing tenniscore sales data...")
        tenniscore = self.load_tenniscore_sales()
        tenniscore.to_csv(self.processed_path / 'tenniscore_processed.csv', index=False)
        
        print("Processing market data...")
        market = self.load_market_data()
        market.to_csv(self.processed_path / 'market_combined.csv', index=False)
        
        print("Processing trends data...")
        trends = self.load_trends_data()
        trends.to_csv(self.processed_path / 'trends_processed.csv', index=False)
        
        print("Processing Challengers impact data...")
        challengers = self.load_challengers_impact()
        challengers.to_csv(self.processed_path / 'challengers_processed.csv', index=False)
        
        print("Creating summary statistics...")
        summary = self.create_summary_stats()
        summary.to_csv(self.processed_path / 'summary_stats.csv', index=False)
        
        print(f"\nProcessing complete! Files saved to {self.processed_path}")
        
        return {
            'tenniscore': tenniscore,
            'market': market,
            'trends': trends,
            'challengers': challengers,
            'summary': summary
        }

if __name__ == "__main__":
    processor = DataProcessor()
    data = processor.process_all()
    
    print("\n=== SUMMARY STATISTICS ===")
    print(data['summary'].T)
    
    print("\n=== TOP TENNISCORE ITEMS ===")
    print(data['tenniscore'].nlargest(5, 'yoy_growth_pct')[['item', 'yoy_growth_pct']])
