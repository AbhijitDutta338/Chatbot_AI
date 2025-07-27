import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseConnection:
    """Firebase Firestore connection manager"""
    
    def __init__(self, service_account_path: Optional[str] = None):
        """
        Initialize Firebase connection
        
        Args:
            service_account_path: Path to Firebase service account JSON file
        """
        self.db = None
        self.service_account_path = service_account_path or self._get_default_service_account_path()
        
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase Admin SDK
                cred = credentials.Certificate(self.service_account_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized successfully")
            
            # Get Firestore client
            self.db = firestore.client()
            logger.info("Firestore client connected successfully")
            
        except FileNotFoundError:
            logger.error(f"Service account file not found: {self.service_account_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    
    def _get_default_service_account_path(self) -> str:
        """Get the default path to the service account file from environment variable"""
        # Get from environment variable
        env_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
        if env_path:
            return env_path
        
        # Fallback to local path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, 'firebase_key.json')
    
    def get_collection(self, collection_name: str):
        """Get a Firestore collection reference"""
        if not self.db:
            raise Exception("Firestore client not initialized")
        return self.db.collection(collection_name)

class BaseModel:
    """Base model for Firestore documents"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.data = data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create model from dictionary"""
        return cls(data)

class User(BaseModel):
    """User model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.name = self.data.get('name')
        self.email = self.data.get('email')
        self.role = self.data.get('role', 'user')
        self.created_at = self.data.get('created_at')
        self.updated_at = self.data.get('updated_at')

class Event(BaseModel):
    """Event model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.title = self.data.get('title')
        self.description = self.data.get('description')
        self.date = self.data.get('date')
        self.location = self.data.get('location')
        self.organizer = self.data.get('organizer')
        self.status = self.data.get('status', 'active')

class Alert(BaseModel):
    """Alert model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.type = self.data.get('type')
        self.message = self.data.get('message')
        self.severity = self.data.get('severity', 'medium')
        self.location = self.data.get('location')
        self.created_at = self.data.get('created_at')
        self.status = self.data.get('status', 'active')

class Incident(BaseModel):
    """Incident model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.type = self.data.get('type')
        self.description = self.data.get('description')
        self.location = self.data.get('location')
        self.reported_by = self.data.get('reported_by')
        self.status = self.data.get('status', 'open')
        self.created_at = self.data.get('created_at')
        self.updated_at = self.data.get('updated_at')

class LostAndFound(BaseModel):
    """Lost and Found model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.item_name = self.data.get('item_name')
        self.description = self.data.get('description')
        self.location_found = self.data.get('location_found')
        self.found_by = self.data.get('found_by')
        self.status = self.data.get('status', 'lost')  # 'lost' or 'found'
        self.created_at = self.data.get('created_at')

class Document(BaseModel):
    """Document model for Firestore"""
    
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data)
        self.id = self.data.get('id')
        self.title = self.data.get('title')
        self.content = self.data.get('content')
        self.type = self.data.get('type')
        self.author = self.data.get('author')
        self.created_at = self.data.get('created_at')
        self.updated_at = self.data.get('updated_at')

class FirestoreService:
    """Service class for Firestore operations"""
    
    def __init__(self):
        self.connection = FirebaseConnection()
        self.db = self.connection.db
    
    def get_all_documents(self, collection_name: str) -> List[Dict[str, Any]]:
        """Get all documents from a collection"""
        try:
            collection_ref = self.db.collection(collection_name)
            docs = collection_ref.stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching documents from {collection_name}: {str(e)}")
            return []
    
    def get_document_by_id(self, collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        try:
            doc_ref = self.db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error fetching document {doc_id} from {collection_name}: {str(e)}")
            return None
    
    def add_document(self, collection_name: str, data: Dict[str, Any]) -> Optional[str]:
        """Add a new document to a collection"""
        try:
            # Add timestamps
            data['created_at'] = datetime.now().isoformat()
            data['updated_at'] = datetime.now().isoformat()
            
            doc_ref = self.db.collection(collection_name).add(data)
            logger.info(f"Document added to {collection_name} with ID: {doc_ref[1].id}")
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Error adding document to {collection_name}: {str(e)}")
            return None
    
    def update_document(self, collection_name: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing document"""
        try:
            data['updated_at'] = datetime.now().isoformat()
            self.db.collection(collection_name).document(doc_id).update(data)
            logger.info(f"Document {doc_id} updated in {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error updating document {doc_id} in {collection_name}: {str(e)}")
            return False
    
    def delete_document(self, collection_name: str, doc_id: str) -> bool:
        """Delete a document"""
        try:
            self.db.collection(collection_name).document(doc_id).delete()
            logger.info(f"Document {doc_id} deleted from {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id} from {collection_name}: {str(e)}")
            return False

# Example usage and testing
def test_firestore_connection():
    """Test the Firestore connection and basic operations"""
    try:
        service = FirestoreService()
        
        # Test getting all documents from different collections
        collections = ['users', 'events', 'alerts', 'incidents', 'lost_and_found', 'documents']
        
        for collection in collections:
            logger.info(f"\n=== {collection.upper()} ===")
            documents = service.get_all_documents(collection)
            logger.info(f"Found {len(documents)} documents")
            
            if documents:
                # Show first document as example
                logger.info("Sample document:")
                logger.info(documents[0])
        
        logger.info("\n=== CONNECTION TEST COMPLETED ===")
        
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")

if __name__ == "__main__":
    # Run the test when script is executed directly
    test_firestore_connection()