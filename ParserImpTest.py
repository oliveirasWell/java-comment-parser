from commentParser.abstract.Parser import Parser

from commentParser.utils.linguage_definitions import java

if __name__ == "__main__":
    parser = Parser("./resources/ObservableUsingTest.java", linguage_definition=java, verbose=False)
    parserOut = parser.parse()

    print("___________________________________________________________________")
    print(parserOut)
    print("___________________________________________________________________")
