from commentParser.abstract.Parser import Parser
from commentParser.linguage_definitions import csharp


class CSharpParser(Parser):
    def __init__(self, file_path, verbose):
        super().__init__(file_path, verbose, csharp)
        print('Get Started')
