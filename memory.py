import streamlit as st
import datetime
import uuid
import pymongo

# --- 1. GLOBAL CACHED CONNECTION FUNCTION ---
# This ensures we connect ONLY ONCE, not every time you refresh.
@st.cache_resource
def get_mongo_collection():
    try:
        # Check if secret exists
        if "MONGO_URI" not in st.secrets:
            st.error("❌ MONGO_URI missing in Secrets!")
            return None

        uri = st.secrets["MONGO_URI"]
        
        # Connect with a timeout so it doesn't hang forever
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Force a check to see if connection works
        client.server_info() 
        
        db = client["research_agent_db"]
        return db["history"]
        
    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")
        return None

class HistoryManager:
    def __init__(self):
        # Load the cached collection
        self.collection = get_mongo_collection()

    def load_history(self):
        """Loads history from MongoDB."""
        if self.collection is None:
            return []
            
        try:
            # Sort by timestamp descending (newest first)
            # We sort in Python to keep it simple, or use .sort() in Mongo
            cursor = self.collection.find({}, {"_id": 0})
            history = list(cursor)
            
            # Optional: Sort locally by timestamp if needed
            # history.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return history
        except Exception as e:
            st.error(f"Error loading history: {e}")
            return []

    def save_entry(self, input_text, mode, final_report, messages):
        """Saves a new research session to MongoDB."""
        if self.collection is None:
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
            st.error(f"Error saving to DB: {e}")
            return None

    def delete_entry(self, entry_id):
        """Deletes a specific entry by ID."""
        if self.collection is not None:
            self.collection.delete_one({"id": entry_id})