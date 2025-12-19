import streamlit as st
import datetime
import uuid
import pymongo

class HistoryManager:
    def __init__(self):
        # We try to get the connection string from Streamlit Secrets
        try:
            self.mongo_uri = st.secrets["MONGO_URI"]
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client["research_agent_db"]
            self.collection = self.db["history"]
            self.is_connected = True
        except Exception:
            self.is_connected = False
            # This allows the app to load locally without crashing, 
            # even if secrets aren't set yet.
            print("⚠️ MongoDB not connected. History will not be saved.")

    def load_history(self):
        """Loads history from MongoDB."""
        if not self.is_connected:
            return []
            
        # Fetch all documents, exclude the internal '_id' field
        try:
            cursor = self.collection.find({}, {"_id": 0})
            history = list(cursor)
            return history
        except Exception as e:
            return []

    def save_entry(self, input_text, mode, final_report, messages):
        """Saves a new research session to MongoDB."""
        if not self.is_connected:
            return None

        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "mode": mode,
            "input": input_text,
            "report": final_report,
            "chat_history": messages
        }
        
        try:
            self.collection.insert_one(entry)
            return entry
        except Exception as e:
            print(f"Error saving: {e}")
            return None

    def delete_entry(self, entry_id):
        """Deletes a specific entry by ID."""
        if self.is_connected:
            self.collection.delete_one({"id": entry_id})