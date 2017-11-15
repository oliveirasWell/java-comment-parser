"""
 Wellington de Oliveira dos Santos

"""


class Scanner:
    def __init__(self, file_path):
        self.actual_line = 0
        self.actual_token = ""
        self.actual_position = -1
        self.file_path = file_path
        file = open(file_path)
        tokens = []
        for line in file:
            raw_line = line.replace('\n', ' \n').replace('//', '// ').replace('/*', '/* ').replace('*/', '*/ ').replace('{', '{ ').replace('}', '} ').split(' ')

            striped_line = [x for x in raw_line if x]

            for word in striped_line:
                if word:
                    tokens.append(word)

        self.tokens = tokens
        self.tokens_len = len(tokens)

    def getNextToken(self):
        if self.actual_position + 1 == self.tokens_len:
            self.actual_token = None
            return False

        if self.tokens[self.actual_position] == '\n':
            self.actual_line = self.actual_line + 1

        self.actual_position = self.actual_position + 1
        self.actual_token = self.tokens[self.actual_position]
        return True

    def getToken(self, token_position):
        if token_position >= self.tokens_len:
            self.actual_token = None
            return ""

        return self.tokens[token_position]


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
        print("----------------------------------------------------------")
        print("Linha do comentário: {} ".format(self.lineStart))
        print("Conteudo:")
        print("{} ".format(" ".join(self.comment)))
        print("Licenca:{} ".format(self.isLicenca))
        print("Classe:{} ".format(self.className))
        print("Metodo:{} ".format(self.methodName))
        print("Field:{} ".format(self.fieldName))

        if self.lineEnd:
            print("Linha final do comentário:{} ".format(self.lineEnd))


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
        print("{}:{} ".format(self.classType, self.className))
        print("Linhas:{} - {} ".format(self.lineStart, self.lineEnd))

    def isEnum(self):
        return self.classType == 'enum'


class Method:
    def __init__(self, methodName, lineStart, lineEnd=None):
        self.lineEnd = lineEnd
        self.lineStart = lineStart
        self.methodName = methodName

    def print(self):
        print("Metodo:{} ".format(self.methodName))
        print("Linhas:{} - {} ".format(self.lineStart, self.lineEnd))


class Element:
    def __init__(self, elementType, elementName, lineStart):
        self.lineStart = lineStart
        self.elementType = elementType
        self.elementName = elementName

    def print(self):
        print("{}:{} ".format(self.elementType, self.elementName))
        print("Linhas:{}".format(self.lineStart))


def main():
    elements = []
    classes = []
    methods = []
    brace_count = 0
    comments = []
    actual_class_stack = []
    actual_method_stack = []
    access_control_modifiers_stack = []
    non_access_control_modifiers_stack = []
    documentation = True
    method_started = False
    brace_count_when_method_started = 0
    all_elements = []

    print('Init')
    scanner = Scanner('resources/.....')

    while scanner.getNextToken():

        if scanner.actual_token == 'package':
            documentation = False
            continue

        if scanner.actual_token == 'import':
            while scanner.actual_token != '\n':
                scanner.getNextToken()
            continue

        if scanner.actual_token == '\n':
            continue

        if scanner.actual_token == 'return':
            continue

        if scanner.actual_token[0] == '@':
            while scanner.actual_token != '\n':
                scanner.getNextToken()
            continue

        if '{' in scanner.actual_token:
            brace_count = brace_count + 1
            continue

        if '}' in scanner.actual_token:
            if method_started and (brace_count_when_method_started == brace_count):

                method = actual_method_stack.pop()
                method.lineEnd = scanner.actual_line
                methods.append(method)

                method_started = False
                brace_count_when_method_started = -1
            elif brace_count == len(actual_class_stack):
                classItem = actual_class_stack.pop()
                classItem.lineEnd = scanner.actual_line
                classes.append(classItem)

            brace_count = brace_count - 1
            continue

        if scanner.actual_token in ['public', 'private', 'proteced']:
            access_control_modifiers_stack.append(scanner.actual_token)
            continue

        if scanner.actual_token in ['static', 'final', 'abstract', 'synchronized', 'volatile']:
            non_access_control_modifiers_stack.append(scanner.actual_token)
            continue

        # declaração de metodo ou elemento
        if scanner.actual_token or scanner.actual_token == 'void':
            if (';' in scanner.getToken(scanner.actual_position + 1) or ('=' in scanner.getToken(scanner.actual_position + 1))) and not method_started:
                elementType = scanner.actual_token
                scanner.getNextToken()
                element = scanner.actual_token
                elementItem = Element(elementType, element, scanner.actual_line)

                all_elements.append(elementItem)
                elements.append(elementItem)

            elif ('(' in scanner.getToken(scanner.actual_position + 2) or ('(' in scanner.getToken(scanner.actual_position + 1))) and not method_started:

                methodName = scanner.actual_token
                while ')' not in scanner.actual_token:
                    scanner.getNextToken()
                    methodName = methodName + ((" " + scanner.actual_token) if scanner.actual_token != '\n' else '')

                actual_method_stack.append(Method(methodName, scanner.actual_line))
                method_started = True
                brace_count_when_method_started = brace_count + 1
                continue

        if scanner.actual_token in ['class', 'enum']:
            classType = scanner.actual_token
            scanner.getNextToken()
            classItem = Class(classType, scanner.actual_token, scanner.actual_line)

            all_elements.append(classItem)
            actual_class_stack.append(classItem)
            continue

        if scanner.actual_token == '//' or scanner.actual_token == '/*':
            commentItem = {}
            is_doc = documentation
            class_name = (actual_class_stack[-1]).className if len(actual_class_stack) else None
            method_name = (actual_method_stack[-1]).methodName if method_started else None

            if scanner.actual_token == '//':
                comment_content = []
                while scanner.actual_token != '\n' and scanner.actual_token is not None:
                    comment_content.append(scanner.actual_token)
                    scanner.getNextToken()
                commentItem = Comment('//', comment_content, scanner.actual_line, scanner.actual_line, isLicenca=is_doc, className=class_name,
                                      methodName=method_name)

            if scanner.actual_token == '/*':
                line_start = scanner.actual_line
                comment_content = [scanner.actual_token]

                while scanner.actual_token != '*/' and scanner.actual_token is not None:
                    scanner.getNextToken()
                    comment_content.append(scanner.actual_token)
                commentItem = Comment('/*', comment_content, line_start, scanner.actual_line, isLicenca=is_doc, className=class_name, methodName=method_name)

            all_elements.append(commentItem)
            comments.append(commentItem)

            continue

    matchCommentsAndElements(all_elements)

    return


def matchCommentsAndElements(allElements):
    for i in range(len(allElements)):

        element = allElements[i]

        if type(element) is Comment and i + 1 < len(allElements):

            nextElement = allElements[i + 1]
            prevElement = allElements[i - 1]

            if element.className is None and type(nextElement) is Class and not element.isLicenca:
                element.className = nextElement.className
            elif element.className is not None and type(nextElement) is Class and nextElement.isEnum:
                element.className = nextElement.className
            elif element.fieldName is None and element.methodName is None and type(prevElement) is Element and element.lineStart == prevElement.lineStart:
                element.fieldName = prevElement.elementName
            elif element.fieldName is None and element.methodName is None and type(nextElement) is Element:
                element.fieldName = nextElement.elementName
            elif element.fieldName is None and element.methodName is None and type(prevElement) is Method and element.lineStart == prevElement.lineStart:
                element.methodName = prevElement.methodName
            elif element.fieldName is None and element.methodName is None and type(nextElement) is Method:
                element.methodName = nextElement.methodName

            element.print()


if __name__ == "__main__":
    main()
