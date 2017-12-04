class Comment:
    def __init__(self, type_of_comment, comment, lineStart, lineEnd, isLicenca, className=None, methodName=None, fieldName=None,
                 type_of_entity=None):
        self.fieldName = fieldName
        self.methodName = methodName
        self.className = className
        self.isLicenca = isLicenca
        self.lineEnd = lineEnd
        self.type_of_entity = type_of_entity
        self.lineStart = lineStart
        self.comment = comment
        self.type_of_comment = type_of_comment
        return

    def print(self):
        return_string = "----------------------------------------------------------\n" + \
               "Linha do comentário: {}\n".format(self.lineStart) + \
               "Conteudo:\n" + \
               "{}\n".format(" ".join(self.comment)) + \
               "Licenca:{}\n".format(self.isLicenca) + \
               "Classe:{}\n".format(self.className) + \
               "Metodo:{}\n".format(self.methodName) + \
               "Field:{}\n".format(self.fieldName)

        if self.lineEnd:
            return_string = return_string + "Linha final do comentário:{}\n".format(self.lineEnd)

        return return_string