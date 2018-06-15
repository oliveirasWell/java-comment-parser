from entities.Class import Class
from entities.Comment import Comment
from entities.Attribute import Attribute
from entities.Method import Method
from commentParser.abstract.Scanner import Scanner


class Parser:
    def __init__(self, file_path, verbose, linguage_definition):
        self.started_import = False
        self.elements = []
        self.classes = []
        self.methods = []
        self.comments = []
        self.class_stack = []
        self.actual_method_stack = []
        self.elements_stack = []
        self.lambdaMethodStack = []
        self.filePath = file_path
        self.brace_count = 0
        self.documentation = True
        self.method_started = False
        self.brace_count_when_method_started = -1
        self.brace_count_when_enum_item_started = -1
        self.waitingForDeclarationEnd = False
        self.waitingForEndParentheses = False
        self.brace_count_when_declaration_started = 0
        self.lambdaMethodStarted = False
        self.isEnumDeclaration = False
        self.inEnumBody = False
        self.elementItemInEnumBody = None
        self.scanner = Scanner(self.filePath, linguage_definition['especial_characters'])
        self.linguage_definition = linguage_definition
        self.single_line_comment_start_token = linguage_definition['single_line_comment']
        self.multi_line_comment_start_token = linguage_definition['multi_line__comment_start']
        self.multi_line_comment_end_token = linguage_definition['multi_line__comment_end']
        self.verbose = verbose
        self.annotationStartStatement = linguage_definition['annotation_start_statement']

    def resolve_comment(self):
        actual_class_stack = self.class_stack
        actual_method_stack = self.actual_method_stack
        all_elements = self.elements_stack
        comments = self.comments
        documentation = self.documentation
        method_started = self.method_started
        scanner = self.scanner
        element_item_in_enum_body = self.elementItemInEnumBody
        comment_item = {}
        is_doc = documentation
        class_name = (actual_class_stack[-1]).className if len(actual_class_stack) else None
        method_name = (actual_method_stack[-1]).methodName if method_started else None
        element_item_in_enum_body = element_item_in_enum_body.attributeName if element_item_in_enum_body is not None else None

        lineComment = '//'
        if scanner.actual_token == lineComment:
            comment_content = []
            while scanner.actual_token != '\n' and scanner.actual_token is not None:
                comment_content.append(scanner.actual_token)
                scanner.getNextToken()

            comment_item = Comment(lineComment, comment_content, scanner.actual_line, scanner.actual_line, isLicenca=is_doc, className=class_name,
                                   methodName=method_name, fieldName=element_item_in_enum_body)

        blockCommentStartStatement = '/*'
        if scanner.actual_token == blockCommentStartStatement:
            line_start = scanner.actual_line
            comment_content = [scanner.actual_token]

            while scanner.actual_token != '*/' and scanner.actual_token is not None:
                scanner.getNextToken()
                comment_content.append(scanner.actual_token)

            comment_item = Comment('%s' % blockCommentStartStatement, comment_content, line_start, scanner.actual_line, isLicenca=is_doc,
                                   className=class_name, methodName=method_name, fieldName=element_item_in_enum_body)

        if comment_item:
            all_elements.append(comment_item)
            comments.append(comment_item)

    def parse(self):

        self.brace_count = 0
        self.documentation = True
        self.method_started = False
        self.brace_count_when_method_started = -1
        self.brace_count_when_enum_item_started = -1
        self.waitingForDeclarationEnd = False
        self.lambdaMethodStarted = False
        self.isEnumDeclaration = False
        self.inEnumBody = False
        self.elementItemInEnumBody = None

        return self.parser_state_machine()

    def is_comment(self, start_comment_types):
        return self.scanner.actual_token in start_comment_types

    def verify_if_have_comment_and_parse(self, start_comment_types):
        if self.is_comment(start_comment_types):
            self.resolve_comment()

    ###########################################################################################################################
    ###########################################################################################################################

    def parser_state_machine(self):
        endDeclarationToken = self.linguage_definition['end_declaration']
        multLineCommentStartToken = self.multi_line_comment_start_token
        singleLineCommentStartToken = self.single_line_comment_start_token
        start_comment_types = [multLineCommentStartToken, singleLineCommentStartToken]
        openBraceStatement = '{'
        closeBraceStatement = '}'
        startStringStatement = '"'
        breakLineStatement = '\n'

        actualToken = None
        contParenteses = 0

        # initial state
        while self.scanner.getNextToken():

            actualToken = self.scanner.actual_token
            self.print_token()

            if self.is_comment(start_comment_types):
                self.resolve_comment()
                continue

            if self.scanner.isActualToken(breakLineStatement):
                continue

            if self.scanner.isInActualToken(openBraceStatement):
                self.resolve_and_add_brace()
                continue

            if self.scanner.isInActualToken(closeBraceStatement):
                self.resolve_remove_brace(endDeclarationToken)
                continue

            if self.scanner.isActualToken(startStringStatement):
                self.resolve_string()
                continue

            if self.scanner.isActualToken('package'):
                self.resolve_documentation()
                continue

            if self.scanner.isActualToken('import'):
                self.resolve_import(endDeclarationToken, start_comment_types)
                continue

            if self.waitingForDeclarationEnd and self.scanner.isActualToken(endDeclarationToken):
                if self.brace_count_when_declaration_started == self.brace_count:
                    self.waitingForDeclarationEnd = False
                    self.brace_count_when_declaration_started = -1
                continue

            # Palavras reservadas
            if self.scanner.actual_token in self.linguage_definition['keywords']:
                continue

            # Palavras reservadas
            if self.scanner.actual_token in self.linguage_definition['ignored_chars']:
                continue

            if self.scanner.isInActualToken(['(', ')']):
                if self.scanner.actual_token == ')':
                    contParenteses = contParenteses - 1

                if self.scanner.actual_token == '(':
                    contParenteses = contParenteses + 1
                continue

            # declaração de classes
            if self.scanner.isInActualToken(['class', 'enum']) and not self.waitingForDeclarationEnd:

                class_type = self.scanner.actual_token
                if class_type == 'enum':
                    self.isEnumDeclaration = True
                    self.inEnumBody = False

                ## PODE ser comentário aqui, vai dar errado.
                self.scanner.getNextToken()

                class_item = Class(class_type, self.scanner.actual_token, self.scanner.actual_line)
                self.elements_stack.append(class_item)
                self.class_stack.append(class_item)

                continue

            # TODO refatorar bem isso pois não faz o menor sentido não voltar pra main
            # DENTRO DO ENUM
            if self.isEnumDeclaration and not self.inEnumBody and not self.waitingForDeclarationEnd:

                # passar isso pra um método resolve
                while self.scanner.actual_token == singleLineCommentStartToken or self.scanner.actual_token == multLineCommentStartToken or self.scanner.actual_token == breakLineStatement:
                    self.resolve_comment()
                    self.scanner.getNextToken()

                if self.scanner.actual_token == ',':
                    continue

                elementItem = Attribute(self.scanner.actual_token, self.scanner.actual_token, self.scanner.actual_line)
                self.elements.append(elementItem)
                self.elements_stack.append(elementItem)
                self.scanner.getNextToken()

                if self.scanner.actual_token == '(':
                    # Get conteudo dentro dos parenteses
                    contParenteses = 0
                    while self.scanner.actual_token != ')' and contParenteses != 0:
                        if self.scanner.actual_token == ')':
                            contParenteses = contParenteses - 1

                        if self.scanner.actual_token == '(':
                            contParenteses = contParenteses + 1

                        self.verify_if_have_comment_and_parse(start_comment_types)

                        self.scanner.getNextToken()

                if self.scanner.actual_token == openBraceStatement:
                    self.inEnumBody = True
                    self.elementItemInEnumBody = elementItem
                    self.brace_count_when_enum_item_started = self.brace_count + 1
                    self.scanner.setPosition(self.scanner.actual_position - 1)

                continue

            if self.scanner.actual_token == '->':
                if self.scanner.getToken(self.scanner.actual_position + 1) == openBraceStatement:
                    self.lambdaMethodStarted = True
                    self.lambdaMethodStack.append({'brace_count': self.brace_count + 1})

                continue

            # Lacos
            if self.scanner.actual_token in ['while', 'if', 'for']:  # loops_keywords
                self.scanner.getNextToken()

                # Get conteudo dentro dos parenteses
                contParenteses = 0
                while self.scanner.actual_token != ')' and contParenteses != 0:
                    if self.scanner.actual_token == ')':
                        contParenteses = contParenteses - 1
                    if self.scanner.actual_token == '(':
                        contParenteses = contParenteses + 1
                    self.verify_if_have_comment_and_parse(start_comment_types)
                    self.scanner.getNextToken()

                continue

            # anotação
            if self.scanner.actual_token[0] == ('%s' % self.annotationStartStatement):
                self.scanner.getNextToken()
                # FIXME criar estrutura para salvar esses parenteses e continuar o parse sem ignorar tudo
                if self.scanner.actual_token == '(':
                    self.waitingForEndParentheses = True
                    contParenteses = 1
                continue

            if self.waitingForEndParentheses and self.scanner.isActualToken(')'):
                contParenteses = contParenteses - 1
                if contParenteses == 0:
                    self.waitingForEndParentheses = False
                    contParenteses = -1
                continue

            # declaração de metodo ou elemento
            if (self.scanner.actual_token or self.scanner.isActualToken('void')):
                if not self.waitingForDeclarationEnd and (endDeclarationToken in self.scanner.getToken(self.scanner.actual_position + 2) or ('=' in self.scanner.getToken(self.scanner.actual_position + 2))) and not self.method_started:
                    elementType = self.scanner.actual_token
                    self.scanner.getNextToken()
                    element = self.scanner.actual_token
                    elementItem = Attribute(elementType, element, self.scanner.actual_line)
                    self.elements_stack.append(elementItem)
                    self.elements.append(elementItem)

                    if '=' in [self.scanner.actual_token, self.scanner.getToken(self.scanner.actual_position + 1)]:

                        print('---element----/')
                        print(element)
                        print('/---element----')

                        self.waitingForDeclarationEnd = True
                        self.brace_count_when_declaration_started = self.brace_count

                        if self.scanner.actual_token == '->':
                            self.scanner.setPosition(self.scanner.actual_position - 1)
                        elif '=' == self.scanner.getToken(self.scanner.actual_position + 1):
                            self.scanner.getNextToken()

                    continue

                elif (not self.scanner.getToken(self.scanner.actual_position - 1) == 'new') and ('(' in [self.scanner.getToken(self.scanner.actual_position + 3), self.scanner.getToken(self.scanner.actual_position + 2), self.scanner.getToken(self.scanner.actual_position + 1)]) and not self.method_started and not (
                        self.waitingForDeclarationEnd and self.brace_count_when_declaration_started == self.brace_count):

                    isAbstract = 'abstract' in [self.scanner.getToken(self.scanner.actual_position - 1), self.scanner.actual_token]

                    methodName = self.scanner.actual_token

                    while ')' not in self.scanner.actual_token:
                        self.scanner.getNextToken()
                        if self.scanner.actual_token == multLineCommentStartToken:
                            self.verify_if_have_comment_and_parse(start_comment_types)
                        else:
                            methodName = methodName + ((" " + self.scanner.actual_token) if self.scanner.actual_token != breakLineStatement else '')

                    methodItem = Method(methodName, self.scanner.actual_line)
                    self.actual_method_stack.append(methodItem)
                    self.elements_stack.append(methodItem)

                    self.method_started = True if not isAbstract else False
                    self.brace_count_when_method_started = self.brace_count + 1 if not isAbstract else self.brace_count_when_method_started
                    continue

            if (self.method_started or self.lambdaMethodStarted or self.waitingForDeclarationEnd) and self.scanner.actual_token is not None:
                continue

        self.__printAllElementsIn__()

        elementsToPrint = self.matchCommentsAndElements(self.elements_stack)

        return elementsToPrint

    ###########################################################################################################################
    ###########################################################################################################################

    def resolve_import(self, endDeclarationToken, start_comment_types):
        self.started_import = True
        while self.scanner.actual_token != endDeclarationToken:
            self.verify_if_have_comment_and_parse(start_comment_types)
            self.scanner.getNextToken()

    def resolve_documentation(self):
        self.documentation = False

    def resolve_string(self):
        self.scanner.getNextToken()
        positionStart = positionEnd = self.scanner.actual_position
        # não mudar o '\\', está assim pq ele compara a sequencia '"\', o caractere de \ é '\\'
        while self.scanner.actual_token != '"' or (self.scanner.actual_token == '"' and self.scanner.getToken(self.scanner.actual_position - 1) == '\\'):
            self.scanner.getNextToken()
            positionEnd = self.scanner.actual_position

        print("/--@--")
        print(positionStart - 1)
        print(positionEnd + 1)
        print(self.scanner.tokens[positionStart - 1:positionEnd + 1])
        print("--@--/")

    def resolve_remove_brace(self, endDeclarationToken):
        if self.method_started and self.brace_count_when_method_started == self.brace_count:
            method = self.actual_method_stack.pop()
            method.lineEnd = self.scanner.actual_line
            self.methods.append(method)
            self.method_started = False
            self.brace_count_when_method_started = -1

        elif self.inEnumBody and self.brace_count_when_enum_item_started == self.brace_count:
            self.brace_count_when_enum_item_started = -1
            self.inEnumBody = False
            self.elementItemInEnumBody = None
            if self.scanner.getToken(self.scanner.actual_position + 1) == endDeclarationToken:
                self.isEnumDeclaration = False

        elif self.lambdaMethodStarted:
            if len(self.lambdaMethodStack) > 0 and self.brace_count == self.lambdaMethodStack[-1]['brace_count']:
                self.lambdaMethodStack.pop()
                if len(self.lambdaMethodStack) == 0:
                    self.lambdaMethodStarted = False
        elif self.brace_count == len(self.class_stack):
            classItem = self.class_stack.pop()
            classItem.lineEnd = self.scanner.actual_line
            self.classes.append(classItem)

        self.brace_count = self.brace_count - 1

    def resolve_and_add_brace(self):
        self.brace_count = self.brace_count + 1

    def print_token(self):
        if self.verbose:
            print("{} -- {}".format(self.scanner.actual_line, self.scanner.actual_token))

    def __printAllElementsIn__(self):
        elements = ""
        for element in self.elements_stack:
            elements = elements + element.print()
        return elements

    def matchCommentsAndElements(self, allElements):

        comments_message = ""

        for i in range(len(allElements)):

            element = allElements[i]

            if type(element) is Comment:

                nextElement = allElements[i + 1] if i + 1 < len(allElements) else None
                prevElement = allElements[i - 1] if i - 1 > 0 else None

                if nextElement and element.className is None and type(nextElement) is Class and not element.isLicenca:
                    element.className = nextElement.className
                elif nextElement and element.className is not None and type(nextElement) is Class and nextElement.isEnum:
                    element.className = nextElement.className
                elif prevElement and element.fieldName is None and element.methodName is None and type(
                        prevElement) is Attribute and element.lineStart == prevElement.lineStart:
                    element.fieldName = prevElement.attributeName
                elif nextElement and element.fieldName is None and element.methodName is None and type(nextElement) is Attribute:
                    element.fieldName = nextElement.attributeName
                elif prevElement and element.fieldName is None and element.methodName is None and type(
                        prevElement) is Method and element.lineStart == prevElement.lineStart:
                    element.methodName = prevElement.methodName
                elif nextElement and element.fieldName is None and element.methodName is None and type(nextElement) is Method:
                    element.methodName = nextElement.methodName

                comments_message = comments_message + element.print()

        return comments_message
