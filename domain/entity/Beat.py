from domain.value_object import Duration

class Beat:
    def __init__(self, duration: Duration):
        self.duration = duration
        self.notes = []