class StateManager:
    def __init__(self):
        self.state = {}

    def update_state(self, session_id: str, key: str, value):
        if session_id not in self.state:
            self.state[session_id] = {}
        self.state[session_id][key] = value

    def get_state(self, session_id: str):
        return self.state.get(session_id, {})

state_manager = StateManager()