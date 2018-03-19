from commentParser.abstract.Parser import Parser
from commentParser.utils.linguage_definitions import java


class JavaParser(Parser):
    def __init__(self, file_path, verbose):
        super().__init__(file_path, verbose, java)
        print('Get Started')
