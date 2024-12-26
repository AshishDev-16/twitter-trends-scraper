from flask import Flask, render_template, jsonify
from scraper import TwitterScraper
from database import DatabaseHandler
import json
from datetime import datetime

app = Flask(__name__)
db = DatabaseHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper')
def run_scraper():
    scraper = None
    try:
        # Create new scraper instance (this will use a new proxy)
        scraper = TwitterScraper()
        trends = scraper.get_trending_topics()
        ip_address = scraper.get_current_ip()
        
        # Save to database
        db.save_trends(trends, ip_address)
        
        # Get the latest record
        latest = db.get_latest_trends()
        
        return jsonify({
            'success': True,
            'trends': trends,
            'timestamp': latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': ip_address,
            'mongodb_record': json.loads(json.dumps(latest, default=str))
        })

    except Exception as e:
        print(f"Error in run_scraper: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    finally:
        if scraper:
            scraper.close()

if __name__ == '__main__':
    app.run(debug=True) 