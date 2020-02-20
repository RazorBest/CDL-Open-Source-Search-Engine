import unittest
from loader import load_words_index_from_directory
from search import search


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

    def template(self, dir, test_input, test_output):
        self.wordsIndex = load_words_index_from_directory(dir)

        input_query = self.load_input(test_input)
        expected_output = self.load_expected_output(test_output)
        output = search(input_query, self.wordsIndex)

        self.assertEqual(output, expected_output)

    def test_search_1(self):
        self.template('example_docs', 'test_cases/test1.in',
                      'test_cases/test1.out')

    def test_search_2(self):
        self.template('example_docs', 'test_cases/test2.in',
                      'test_cases/test2.out')

    def test_search_3(self):
        self.template('example_docs', 'test_cases/test3.in',
                      'test_cases/test3.out')

    def test_search_4(self):
        self.template('example_docs', 'test_cases/test4.in',
                      'test_cases/test4.out')

    def test_search_5(self):
        self.template('example_docs', 'test_cases/test5.in',
                      'test_cases/test5.out')

    def test_search_6(self):
        self.template('example_docs', 'test_cases/test6.in',
                      'test_cases/test6.out')

    def test_search_7(self):
        self.template('example_docs', 'test_cases/test7.in',
                      'test_cases/test7.out')


if __name__ == '__main__':
    unittest.main()
