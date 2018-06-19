import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commentParser.abstract.Parser import Parser
from commentParser.utils.linguage_definitions import java

data = [
    ('Action.java', 'action.txt'),
    ('CallableAsyncPerf.java', 'callable_async_perf.txt'),
    ('Content.java', 'content.txt'),
    ('ContentAction.java', 'content_action.txt'),
    ('FailProcessorTests.java', 'fail_processor_tests.txt'),
    ('ForEachProcessorTests.java', 'for_each_processor_tests.txt'),
    ('GrokProcessorFactoryTests.java', 'grok_processor_factory_tests.txt'),
    ('InputWithIncrementingInteger.java', 'input_with_incrementing_integer.txt'),
    ('TestLambdaVelho.java', 'test_lambda_velho.txt'),
    ('OperationConcat.java', 'operation_concat.txt'),
    ('DebugNotification.java', 'debug_notification.txt'),
    ('RxSuspendableClassifier.java', 'rx_suspendable_classifier.txt'),
    ('ObservableUsingTest.java', 'ObservableUsingTest.txt'),
    ('ReplicationType.java', 'ReplicationType.txt'),
    ('NettyTransportManagement.java', 'NettyTransportManagement.txt'),
    ('XContentRestResponse.java', 'XContentRestResponse.txt'),
    ('HistogramFacet.java', 'HistogramFacet.txt'),
    ('SizeUnit.java', 'SizeUnit.txt'),
]


def open_file(path):
    file = open(path, 'r')
    string_expected = ""
    for line in file:
        string_expected = string_expected + line
    file.close()
    return string_expected


def create_test_func(javaParserPath, expectedPath):
    def _test_func(self):
        string_expected = open_file('testsoutputs/' + expectedPath)
        parser = Parser('../resources/' + javaParserPath, True, linguage_definition=java)
        parserOut = parser.parse()
        self.assertEqual(string_expected, parserOut)

    return _test_func


class TestParse(unittest.TestCase):
    maxDiff = None


for i, (found, expected) in enumerate(data):
    setattr(TestParse, 'test_data_%s' % data[i][0], create_test_func(found, expected))

if __name__ == '__main__':
    unittest.main()
