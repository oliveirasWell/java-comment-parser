class Method:
    def __init__(self, methodName, lineStart, lineEnd=None):
        self.lineEnd = lineEnd
        self.lineStart = lineStart
        self.methodName = methodName

    def print(self):
        return "----------------------------------------------------------\n" + \
               "Metodo:{}\n".format(self.methodName) + \
               "Linhas:{} -{} \n".format(self.lineStart, self.lineEnd)
