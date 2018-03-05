from commentParser.abstract.Parser import Parser
from commentParser.utils.linguage_definitions import shellscript


class ShellScriptParser(Parser):
    def __init__(self, file_path, verbose):
        super().__init__(file_path, verbose, shellscript)
        print('Get Started')
