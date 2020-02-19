from bitstring import BitArray
from loader import load_words_index
import re


def token_split(query):
    """Split the query into tokens delimited 
        by '(', ')', '||', '&&', '!' or whitespaces
    """
    # Split into tokens delimited by spaces
    query = re.split(r'\s+', query)

    tokens = []
    for token in query:
        token = re.split(r'([\!\(\)]|&{2}|\|{2})', token)
        # Remove empty strings from list
        token = list(filter(None, token))
        tokens.extend(token)

    return tokens


def solve_query(query, wordsIndex):
    """Return a list of files that match the query"""
    result = BitArray()
    query = query.lower()

    tokens = token_split(query)

    return result


if __name__ == '__main__':
    wordsIndex = load_words_index('example_docs')
    query = 'Linus   || Torvalds   &&kernel && C || (!cat && !dog)'
    solve_query(query, wordsIndex)
