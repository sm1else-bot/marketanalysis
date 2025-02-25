
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def get_stock_news(company_name, days=7):
    """Fetch recent news headlines about a company"""
    try:
        # Initialize NewsAPI client (free API key)
        newsapi = NewsApiClient(api_key='4e6ee638f5534c4f8a7b3c7878c81127')
        
        # Get date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        # Search for news
        news = newsapi.get_everything(
            q=f"{company_name} stock",
            language='en',
            from_param=from_date.strftime('%Y-%m-%d'),
            to=to_date.strftime('%Y-%m-%d'),
            sort_by='relevancy'
        )
        
        # Format response
        news_items = []
        for article in news['articles'][:5]:
            news_items.append({
                "headline": article['title'],
                "source": article['source']['name']
            })
            
        return news_items
        
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []
