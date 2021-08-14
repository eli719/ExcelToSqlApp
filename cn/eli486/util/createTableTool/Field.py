class Field:
    def __init__(self, name, comment,kinds, isEmpty,  constrainType, constrainName, indexType, indexName):
        self._comment = comment
        self._isEmpty = isEmpty
        self._indexName = indexName
        self._indexType = indexType
        self._constrainName = constrainName
        self._constrainType = constrainType
        self._name = name
        self._kinds = kinds

    @property
    def name(self):
        return self._name

    @property
    def is_empty(self):
        return self._isEmpty

    @property
    def comment(self):
        return self._comment

    @property
    def constrainType(self):
        return self._constrainType

    @property
    def constrainName(self):
        return self._constrainName

    @property
    def indexType(self):
        return self._indexType

    @property
    def indexName(self):
        return self._indexName

    @property
    def kinds(self):
        return self._kinds

    def __repr__(self):
        return ','.join(str(item) for item in (
            self.name, self._comment,self._kinds, self._isEmpty,   self._constrainType, self._constrainName,
            self._indexType, self._indexName))
