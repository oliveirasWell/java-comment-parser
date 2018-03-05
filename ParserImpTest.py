from commentParser.abstract.Parser import Parser

if __name__ == "__main__":
    parser = Parser("./resources/CharMatcherBenchmark.java", True)
    parserOut = parser.parse()

    print("___________________________________________________________________")
    print(parserOut)
    print("___________________________________________________________________")
