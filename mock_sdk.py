# mock_sdk.py
class MockResponse:
    def __init__(self):
        self.context = "### Patient Summary\n- Allergy: Penicillin\n- History: ACL Surgery (2022)\n- Recent: Chest pain when climbing stairs."

class MockDeltaMemory:
    async def ingest(self, content, options=None):
        print(f"[SDK MOCK] Ingesting: {content[:30]}...")
        return {"status": "success", "facts": ["Allergy detected"]}

    async def recall(self, query):
        print(f"[SDK MOCK] Recalling for: {query}")
        return MockResponse()