# mock_sdk.py

class MockDeltaMemory:
    async def ingest(self, content, options=None):
        print(f"[SDK MOCK] Ingesting: {content[:30]}...")
        return {"status": "success"}

    async def recall(self, query):
        print(f"[SDK MOCK] Recalling for: {query}")
        return MockResponse()

    async def graph(self, patient_id):
        """
        Returns the Nodes and Edges for the Patient's medical history.
        Matches the interface expected by knowledge-graph.tsx.
        """
        return {
            "nodes": [
                {"id": "p1", "name": "Sarah", "node_type": "concept"},
                {"id": "s1", "name": "Chest Pain", "node_type": "fact", "salience": 0.9},
                {"id": "a1", "name": "Penicillin Allergy", "node_type": "fact"},
                {"id": "d1", "name": "Cardiology", "node_type": "concept"}
            ],
            "edges": [
                {"from": "p1", "to": "s1", "relation_type": "experiencing", "weight": 1},
                {"from": "p1", "to": "a1", "relation_type": "has_allergy", "weight": 1},
                {"from": "s1", "to": "d1", "relation_type": "referred_to", "weight": 0.8}
            ]
        }