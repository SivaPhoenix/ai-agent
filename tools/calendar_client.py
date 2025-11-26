# calendar_client.py
class MockCalendarClient:
    def __init__(self):
        self.events = []

    def create_events(self, events):
        for e in events:
            self.events.append(e)
        return True
