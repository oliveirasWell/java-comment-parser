class Attribute:
    def __init__(self, attributeType, attributeName, lineStart):
        self.lineStart = lineStart
        self.attributeType = attributeType
        self.attributeName = attributeName

    def print(self):
        return "----------------------------------------------------------\n" + \
               "{}:{}\n".format(self.attributeType, self.attributeName) + \
               "Linhas:{}\n".format(self.lineStart)
