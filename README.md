# Twitter Trends Scraper

## Project Overview
The application scrapes the top 5 trending topics from Twitter's "What's Happening" section and stores them in a MongoDB database. Each request is made through a different IP address using ProxyMesh to avoid rate limiting.

### Features
- Scrapes top 5 trending topics from Twitter
- Uses ProxyMesh for IP rotation
- Stores results in MongoDB
- Clean web interface to view results
- Shows timestamp and IP address for each query

## Technologies Used
- Python 3.x
- Flask
- Selenium WebDriver
- MongoDB
- ProxyMesh
- HTML/CSS/JavaScript

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/AshishDev-16/twitter-trends-scraper.git
cd twitter-trends-scraper 
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env` file
```env
PROXYMESH_USERNAME=your_proxymesh_username
PROXYMESH_PASSWORD=your_proxymesh_password
MONGODB_URI=your_mongodb_uri
```

4. Run the application
```bash
python app.py
```

## Project Structure

- `app.py`: Main Flask application
- `scraper.py`: Scraping logic
- `database.py`: Database operations
- `cleanup.py`: Cleanup script for screenshots
- `requirements.txt`: Dependencies
- `templates/index.html`: Web interface
- `static/styles.css`: CSS for the web interface

## Usage
1. Start the Flask server
2. Navigate to `http://localhost:5000` in your browser
3. Click the "Run Script" button to fetch current trending topics
4. View the results, including:
   - Top 5 trending topics
   - Timestamp of the query
   - IP address used for the request
   - MongoDB record details

## Notes
- Ensure you have valid ProxyMesh credentials
- MongoDB connection string should point to a valid MongoDB instance
- Chrome WebDriver is required for Selenium

