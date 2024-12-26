from pymongo import MongoClient
from datetime import datetime
import uuid

class DatabaseHandler:
    def __init__(self):
        # Direct connection without any special options
        self.client = MongoClient("mongodb+srv://ashishkadu2123:LYWWAh61G8UoUcaG@cluster0.rkotycz.mongodb.net/")
        self.db = self.client.twitter_trends
        self.collection = self.db.trends
        # Test connection
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def save_trends(self, trends, ip_address):
        try:
            # Ensure we have 5 trends
            while len(trends) < 5:
                trends.append(f"Trending {len(trends) + 1}")

            # Create document
            document = {
                '_id': str(uuid.uuid4()),
                'nameoftrend1': str(trends[0]),
                'nameoftrend2': str(trends[1]),
                'nameoftrend3': str(trends[2]),
                'nameoftrend4': str(trends[3]),
                'nameoftrend5': str(trends[4]),
                'timestamp': datetime.now(),
                'ip_address': str(ip_address)
            }

            # Insert document
            result = self.collection.insert_one(document)
            print(f"Saved trends with ID: {result.inserted_id}")
            return result

        except Exception as e:
            print(f"Error saving trends: {str(e)}")
            raise

    def get_latest_trends(self):
        try:
            return self.collection.find_one(sort=[('timestamp', -1)])
        except Exception as e:
            print(f"Error getting latest trends: {str(e)}")
            raise

    def __del__(self):
        try:
            if hasattr(self, 'client'):
                self.client.close()
        except:
            pass 