

class Control:
    def __init__(self):
        self.progress_value = 0
        self.tick_start_state = False
        self.string_status = ""
        self.tick_time = 0
        self.string_error_value = ""
        self.error_show = False
        self.error_state = False

    def reset_tick_time(self):
        pass
