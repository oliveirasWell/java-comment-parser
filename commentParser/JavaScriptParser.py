from pygments.lexers import javascript

from commentParser.abstract.Parser import Parser


class JavaScriptParser(Parser):
    def __init__(self, file_path, verbose):
        super().__init__(file_path, verbose, javascript)
        print('Get Started')
