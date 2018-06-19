from commentParser.abstract.Parser import Parser

from commentParser.utils.linguage_definitions import java

if __name__ == "__main__":
    parser = Parser("./resources/JmxService.java", linguage_definition=java, verbose=True)
    parserOut = parser.parse()

    print("___________________________________________________________________")
    print(parserOut)
    print("___________________________________________________________________")
