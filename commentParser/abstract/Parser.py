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
        self.waitingForDeclarationEnd = False
        self.waitingForEndParentheses = False
        self.lambdaMethodStarted = False
        self.isEnumDeclaration = False
        self.inEnumBody = False
        self.elementItemInEnumBody = None
        self.isInStaticInitBlock = False

        self.brace_count_when_method_started = -1
        self.brace_count_when_enum_item_started = -1
        self.brace_count_when_static_block_started = -1
        self.brace_count_when_declaration_started = -1

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
        startCharStatement = '\''
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
            if self.scanner.isActualToken(startCharStatement):
                self.resolve_char()
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
                contParenteses = self.resolveParentheses(contParenteses)
                continue

            # anotação
            if self.scanner.actual_token[0] == ('%s' % self.annotationStartStatement):
                contParenteses = self.resolveAnotation(contParenteses)
                continue

            if self.waitingForEndParentheses and self.scanner.isActualToken(')'):
                contParenteses = contParenteses - 1
                if contParenteses == 0:
                    self.waitingForEndParentheses = False
                    contParenteses = -1
                continue

            if self.scanner.isActualToken('static'):

                if self.scanner.getNextPositionToken() in [singleLineCommentStartToken, multLineCommentStartToken]:
                    self.scanner.getNextToken()
                    self.resolve_comment_recursive(breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken)

                if self.scanner.getNextPositionToken() == openBraceStatement:
                    self.scanner.getNextToken()
                    self.isInStaticInitBlock = True
                    self.brace_count_when_static_block_started = self.brace_count + 1
                    self.resolve_and_add_brace()
                continue

            # declaração de classes
            if self.scanner.isInActualToken(['class', 'enum', 'interface']) and not self.waitingForDeclarationEnd:

                class_type = self.scanner.actual_token
                if class_type == 'enum':
                    self.isEnumDeclaration = True
                    self.inEnumBody = False

                if self.scanner.getNextPositionToken() in [singleLineCommentStartToken, multLineCommentStartToken]:
                    self.scanner.getNextToken()
                    self.resolve_comment_recursive(breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken)

                self.scanner.getNextToken()

                class_item = Class(class_type, self.scanner.actual_token, self.scanner.actual_line)
                self.elements_stack.append(class_item)
                self.class_stack.append(class_item)

                continue

            # TODO refatorar bem isso pois não faz o menor sentido não voltar pra main
            # DENTRO DO ENUM
            if self.isEnumDeclaration and not self.inEnumBody and not self.waitingForDeclarationEnd and not self.method_started:

                self.resolve_comment_recursive(breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken)

                if self.scanner.actual_token == ',':
                    continue

                elementItem = Attribute(self.scanner.actual_token, self.scanner.actual_token, self.scanner.actual_line)
                self.elements.append(elementItem)
                self.elements_stack.append(elementItem)

                if self.scanner.getNextPositionToken() == '(':
                    self.scanner.getNextToken()

                    # Get conteudo dentro dos parenteses
                    contParenteses = 0
                    while self.scanner.actual_token != ')' and contParenteses != 0:
                        contParenteses = self.resolveParentheses(contParenteses)
                        self.verify_if_have_comment_and_parse(start_comment_types)
                        if self.scanner.isInActualToken(openBraceStatement):
                            self.resolve_and_add_brace()
                        elif self.scanner.isInActualToken(closeBraceStatement):
                            self.resolve_remove_brace(endDeclarationToken)
                        elif self.scanner.isActualToken(startStringStatement):
                            self.resolve_string()
                        elif self.scanner.isActualToken(startCharStatement):
                            self.resolve_char()

                        self.scanner.getNextToken()

                self.resolve_comment_recursive(breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken)

                if self.scanner.getNextPositionToken() == ';':
                    self.scanner.getNextToken()
                    self.isEnumDeclaration = False
                    continue

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
                    contParenteses = self.resolveParentheses(contParenteses)
                    self.verify_if_have_comment_and_parse(start_comment_types)
                    self.scanner.getNextToken()

                continue

            # declaração de metodo ou elemento
            if (self.scanner.actual_token or self.scanner.isActualToken('void')):

                has_parentheses = ('(' in [self.scanner.getToken(self.scanner.actual_position + 3), self.scanner.getToken(self.scanner.actual_position + 2), self.scanner.getToken(self.scanner.actual_position + 1)])

                position_aspas = None
                position_aspas_duplas = None
                position_parentheses = None
                for i in range(3):
                    position_parentheses = i if '(' == self.scanner.getToken(self.scanner.actual_position + i) and position_parentheses is None else position_parentheses
                    position_aspas_duplas = i if '"' == self.scanner.getToken(self.scanner.actual_position + i) and position_aspas_duplas is None else position_aspas_duplas
                    position_aspas = i if '\'' == self.scanner.getToken(self.scanner.actual_position + i) and position_aspas is None else position_aspas

                if not self.waitingForDeclarationEnd \
                        and not self.isInStaticInitBlock \
                        and (endDeclarationToken in self.scanner.getToken(self.scanner.actual_position + 2) or ('=' in self.scanner.getToken(self.scanner.actual_position + 2))) and not self.method_started:

                    elementType = self.scanner.actual_token
                    self.scanner.getNextToken()
                    element = self.scanner.actual_token
                    elementItem = Attribute(elementType, element, self.scanner.actual_line)
                    self.elements_stack.append(elementItem)
                    self.elements.append(elementItem)

                    if '=' in [self.scanner.actual_token, self.scanner.getToken(self.scanner.actual_position + 1)]:

                        if self.verbose:
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

                elif (not self.scanner.getToken(self.scanner.actual_position - 1) == 'new') \
                        and has_parentheses \
                        and not self.method_started \
                        and not self.isInStaticInitBlock \
                        and not (self.waitingForDeclarationEnd and self.brace_count_when_declaration_started == self.brace_count):

                    if (position_aspas_duplas is not None and position_parentheses is not None and position_aspas_duplas < position_parentheses) \
                            or (position_aspas is not None and position_parentheses is not None and (position_aspas + 1) == position_parentheses):
                        continue

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

                    if self.method_started and self.verbose:
                        print("/***** method started")
                        print(methodItem.methodName)
                        print("/***** method end")

                    if self.scanner.getNextPositionToken() == endDeclarationToken:
                        self.method_started = False
                    else:
                        self.brace_count_when_method_started = self.brace_count + 1 if not isAbstract else self.brace_count_when_method_started

                    continue

            if (self.method_started or self.isInStaticInitBlock or self.lambdaMethodStarted or self.waitingForDeclarationEnd) and self.scanner.actual_token is not None:
                continue

        self.__printAllElementsIn__()

        elementsToPrint = self.matchCommentsAndElements(self.elements_stack)

        return elementsToPrint

    def resolve_comment_recursive(self, breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken):
        # passar isso pra um método resolve
        if self.scanner.actual_token in [singleLineCommentStartToken, multLineCommentStartToken]:
            self.resolve_comment()
            self.scanner.getNextToken()
            self.resolve_comment_recursive(breakLineStatement, multLineCommentStartToken, singleLineCommentStartToken)

    def resolveAnotation(self, contParenteses):
        self.scanner.getNextToken()
        if self.scanner.actual_token == '(':
            self.waitingForEndParentheses = True
            contParenteses = 1
        return contParenteses

    ###########################################################################################################################
    ###########################################################################################################################

    def resolveParentheses(self, contParenteses):
        if self.scanner.actual_token == ')':
            contParenteses = contParenteses - 1
        if self.scanner.actual_token == '(':
            contParenteses = contParenteses + 1
        return contParenteses

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
        # não mudar o '\\', está assim pq ele compara a sequencia '"\', o caractere de \ é '\\' só funciona assim não mexe plmds
        while self.scanner.actual_token != '"' or (self.scanner.actual_token == '"' and self.scanner.getToken(self.scanner.actual_position - 1) == '\\'):
            self.scanner.getNextToken()
            positionEnd = self.scanner.actual_position

        if self.verbose:
            print("/--@--")
            print(positionStart - 1)
            print(positionEnd + 1)
            print(self.scanner.tokens[positionStart - 1:positionEnd + 1])
            print("--@--/")

    def resolve_char(self):
        self.scanner.getNextToken()
        positionStart = positionEnd = self.scanner.actual_position
        # não mudar o '\\', está assim pq ele compara a sequencia '"\', o caractere de \ é '\\' só funciona assim não mexe plmds

        while self.scanner.actual_token != '\'' or (self.scanner.actual_token == '\'' and self.scanner.getToken(self.scanner.actual_position - 1) == '\\'):
            self.scanner.getNextToken()
            positionEnd = self.scanner.actual_position

        if self.verbose:
            print("/--@-- char")
            print(positionStart - 1)
            print(positionEnd + 1)
            print(self.scanner.tokens[positionStart - 1:positionEnd + 1])
            print("--@--/")

    def resolve_remove_brace(self, endDeclarationToken):

        if self.verbose:
            print('/****** brace out')
            print(self.brace_count - 1)
            print('******/')

        if self.isInStaticInitBlock and self.brace_count_when_static_block_started == self.brace_count:
            self.brace_count_when_static_block_started = -1
            self.isInStaticInitBlock = False

        elif self.method_started and self.brace_count_when_method_started == self.brace_count:

            if self.verbose:
                print("/drop method declaration")
                print(self.scanner.actual_line)
                print("drop method declaration/")

            method = self.actual_method_stack.pop()
            method.lineEnd = self.scanner.actual_line
            self.methods.append(method)
            self.method_started = False
            self.brace_count_when_method_started = -1

        elif self.inEnumBody and self.brace_count_when_enum_item_started == self.brace_count:

            if self.verbose:
                print("/drop enum declaration")
                print(self.scanner.actual_line)
                print("drop enum declaration/")

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

            if self.verbose:
                print("poped classes")
                print(self.scanner.actual_line)
                print(classItem.className)

        self.brace_count = self.brace_count - 1

    def resolve_and_add_brace(self, element_item=None):

        if self.verbose:
            print('/****** brace in')
            print(self.brace_count + 1)
            print('******/')

        self.brace_count = self.brace_count + 1

        if self.isEnumDeclaration:
            if element_item:
                self.elementItemInEnumBody = element_item
                self.inEnumBody = True
                self.brace_count_when_enum_item_started = self.brace_count

            return

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
