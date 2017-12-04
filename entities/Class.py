class Class:
    def __init__(self, classType, className, lineStart, lineEnd=None, elements=None, methods=None):

        if elements is None:
            elements = []

        if methods is None:
            methods = []

        self.classType = classType
        self.lineEnd = lineEnd
        self.lineStart = lineStart
        self.className = className
        self.elements = elements
        self.methods = methods

    def print(self):
        return "----------------------------------------------------------\n" \
               + "{}:{}\n".format(self.classType, self.className) \
               + "Linhas:{} - {}\n".format(self.lineStart, self.lineEnd)

    def isEnum(self):
        return self.classType == 'enum'
