class NavigationHistory:
    def __init__(self):
        self.history_back = []
        self.history_forward = []
        self.current_filepath = None

    def open_file(self, filepath, save_to_history=True):
        if save_to_history and self.current_filepath:
            self.history_back.append(self.current_filepath)
            self.history_forward.clear()
        self.current_filepath = filepath

    def go_back(self):
        if not self.can_go_back():
            return None
        prev_file = self.history_back.pop()
        if self.current_filepath:
            self.history_forward.append(self.current_filepath)
        self.current_filepath = prev_file
        return prev_file

    def go_forward(self):
        if not self.can_go_forward():
            return None
        next_file = self.history_forward.pop()
        if self.current_filepath:
            self.history_back.append(self.current_filepath)
        self.current_filepath = next_file
        return next_file

    def can_go_back(self):
        return len(self.history_back) > 0

    def can_go_forward(self):
        return len(self.history_forward) > 0
