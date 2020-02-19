import unittest
from loader import load_words_index
from query import search


class TestQueryModule(unittest.TestCase):

    def load_input(self, path):
        f = open(path, 'r')
        file_input = f.read()
        f.close()
        return file_input

    def load_expected_output(self, path):
        f = open(path)
        expected_output = f.readlines()
        expected_output = [x.strip() for x in expected_output]
        f.close()
        return expected_output

    def test_search_1(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test1.in")
        expected_output = self.load_expected_output("test_cases/test1.out")
        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_2(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test2.in")
        expected_output = self.load_expected_output("test_cases/test2.out")
        output = search(input_query, self.wordsIndex)

        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_3(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test3.in")
        expected_output = self.load_expected_output("test_cases/test3.out")
        output = search(input_query, self.wordsIndex)

        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_4(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test4.in")
        expected_output = self.load_expected_output("test_cases/test4.out")
        output = search(input_query, self.wordsIndex)

        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_5(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test5.in")
        expected_output = self.load_expected_output("test_cases/test5.out")
        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_6(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test6.in")
        expected_output = self.load_expected_output("test_cases/test6.out")
        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_7(self):
        self.wordsIndex = load_words_index('example_docs')

        input_query = self.load_input("test_cases/test7.in")
        expected_output = self.load_expected_output("test_cases/test7.out")
        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
