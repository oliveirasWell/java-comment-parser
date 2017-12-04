from commentParser.Parser import Parser

if __name__ == "__main__":
    parser = Parser("./resources/InputWithIncrementingInteger.java", False)
    parserOut = parser.parse()

    print("___________________________________________________________________")
    print(parserOut)
    print("___________________________________________________________________")
