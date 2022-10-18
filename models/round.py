class Round:
    def __init__(self, name):
        self._name = name
        self._matchs = []

    def add_match(self, match):
        self._matchs.append(match)

    def set_begin(self, begin):
        self._date_begin = begin

    def set_end(self, end):
        self._date_end = end

    @property
    def get_round(self):
        return self
