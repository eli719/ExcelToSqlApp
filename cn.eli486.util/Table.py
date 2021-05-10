class Table:
    def __init__(self, name, comment, fields):
        self._comment = comment
        self._name = name
        self._fields = fields

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def fields(self):
        return self._fields

    @comment.setter
    def comment(self, value):
        self._comment = value

    @name.setter
    def name(self, value):
        self._name = value

    @fields.setter
    def fields(self, value):
        self._fields = value

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     if self._i == 0:
    #         return self.fields[self._i]
    #     self._i += 1
