from bitstring import BitArray
from loader import load_words_index
import re

DELIMITERS = r'([\!\(\)]|\&{2}|\|{2})'


def token_split(query):
    """Split the query into tokens delimited
        by '(', ')', '||', '&&', '!' or whitespaces
    """
    # Split into tokens delimited by spaces
    query = re.split(r'\s+', query)

    tokens = []
    for token in query:
        token = re.split(DELIMITERS, token)
        # Remove empty strings from list
        token = list(filter(None, token))
        tokens.extend(token)

    return tokens


def is_word(s):
    return not re.match(DELIMITERS)


def evaluate_expr(expr, wordsIndex):
    """Evaluate the expression using the logical 
        operations from BitArray
    """
    result = BitArray()

    previousBits = BitArray()
    negate = False
    state = ''
    word = ''
    for token in tokens:
        if is_word(token):
            if token in wordsIndex:
                currentBits = wordsIndex[token]
            else:
                currentBits = BitArray()

            if negate:
                currentBits = ~currentBits

            if state == '&&':
                result &= currentBits
            elif state = '||':
                result |= currentBits

            negate = False
        elif token == '!':
            negate = True
        elif re.match(r'\&{2}\|{2}|\!', token):
            state = token
        # TODO parantheses

    return result


def solve_query(query, wordsIndex):
    """Return a list of files that match the query"""

    query = query.lower()
    tokens = token_split(query)
    result = evaluate_expr(tokens, wordsIndex)

    return result


if __name__ == '__main__':
    wordsIndex = load_words_index('example_docs')
    query = 'Linus   || Torvalds   &&kernel && C || (!cat && !dog)'
    solve_query(query, wordsIndex)
