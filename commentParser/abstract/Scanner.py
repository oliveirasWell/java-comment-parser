class Scanner:
    def __init__(self, file_path, special_characteres_list):
        self.actual_line = 0
        self.actual_token = ""
        self.actual_position = -1
        self.file_path = file_path
        file = open(file_path)
        tokens = []

        for line in file:

            line_of_loop = line

            for special_character in special_characteres_list:
                line_of_loop = line_of_loop.replace(special_character, ' ' + special_character + ' ')

            raw_line = line_of_loop.split(' ')

            striped_line = [x for x in raw_line if x]

            for word in striped_line:
                if word:
                    tokens.append(word)
        file.close()
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

    def getNextPositionToken(self):
        return self.getToken(token_position=self.actual_position+1)

    def getToken(self, token_position):
        if token_position >= self.tokens_len:
            self.actual_token = None
            return ""

        return self.tokens[token_position]

    def setPosition(self, newPosition):
        if newPosition < self.tokens_len:
            self.actual_position = newPosition
        return

    def isInActualToken(self, token):
        if type(token) is list:
            return self.actual_token in token

        return token in self.actual_token

    def isActualToken(self, token):
        return token == self.actual_token
