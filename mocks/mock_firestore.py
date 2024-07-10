import logging

class MockFirestore:
    def __init__(self):
        self.data = {}  # Store mock data as a dictionary
        self.logger = logging.getLogger(__name__)  # Get a logger for this class

    def collection(self, collection_name):
        print(f"MockFirestore: collection('{collection_name}') called")
        self.logger.debug(f"MockFirestore: collection('{collection_name}') called")
        return MockCollection(self.data, collection_name)

    def document(self, document_id):
        return MockDocument(self.data, document_id)

class MockCollection:
    def __init__(self, data, collection_name):
        self.data = data
        self.collection_name = collection_name

    def document(self, document_id):
        return MockDocument(self.data, document_id)

    def add(self, data):
        # Simulate adding a document
        document_id = generate_mock_document_id()  # Implement your own ID generation
        self.data[self.collection_name] = self.data.get(self.collection_name, {})
        self.data[self.collection_name][document_id] = data
        return MockDocument(self.data, document_id)

class MockDocument:
    def __init__(self, data, document_id):
        self.data = data
        self.document_id = document_id

    def get(self):
        # Simulate getting a document
        return self.data.get(self.document_id, None)

    def set(self, data):
        # Simulate setting a document
        self.data[self.document_id] = data

    def update(self, data):
        # Simulate updating a document
        self.data[self.document_id].update(data)

def generate_mock_document_id():
    # Implement your own logic to generate mock document IDs
    return 'mock_document_id'
