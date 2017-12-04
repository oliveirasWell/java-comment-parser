import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commentParser.Parser import Parser


class TestStringMethods(unittest.TestCase):
    maxDiff = None

    def test_class_declaration(self):
        string_expected = self.openFileAndReturnString('testsoutputs/class_declaration.txt')
        parser = Parser('../resources/ClassDeclaration.java', False)
        parserOut = parser.parse()
        self.assertEqual(string_expected, parserOut)

    def openFileAndReturnString(self, path):
        file = open(path, 'r')
        string_expected = ""
        for line in file:
            string_expected = string_expected + line
        file.close()
        return string_expected


if __name__ == '__main__':
    unittest.main()
