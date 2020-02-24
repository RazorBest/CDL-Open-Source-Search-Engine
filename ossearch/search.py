from bitstring import BitArray
from .loader import load_words_index_from_directory
from .loader import STOPWORDS
import re
import collections
import itertools


PARANTHESES = r'\(|\)'
OPERATORS = r'\!|\&{2}|\|{2}'
DELIMITERS = '(' + PARANTHESES + '|' + OPERATORS + ')'


def token_split(query):
    """Split the query into tokens delimited
        by '(', ')', '||', '&&', '!' or whitespaces
    """
    # Split into tokens delimited by spaces
    query = re.split(r'\s+', query)

    tokens = []
    for token in query:
        # Split by '(', ')', '||', '&&', '!'
        token = re.split(DELIMITERS, token)
        # Remove empty strings from list
        token = list(filter(None, token))
        tokens.extend(token)

    return tokens


def is_word(s):
    return not re.match(DELIMITERS, s)


def consume(iterator, n):
    '''Advance the iterator n-steps ahead. If n is none, consume entirely.'''
    collections.deque(itertools.islice(iterator, n), maxlen=0)


def find_closing_paranthesis(tokens):
    """Return index of the closing paranthesis"""
    depth = 0

    for index, token in enumerate(tokens):
        if token == '(':
            depth += 1
        elif token == ')':
            depth -= 1
        if depth == 0:
            return index

    return len(tokens)


def apply_operator(result, currentBits, negate, state):
    if negate:
        currentBits = ~currentBits

    if state == '&&':
        result &= currentBits
    elif state == '||':
        result |= currentBits
    else:
        result = currentBits.copy()

    return result


def evaluate_expr(expr, wordsIndex):
    """Evaluate the expression using the logical 
        operations from BitArray.
        The expression must've been split in tokens.
    """
    # Init variables
    result = BitArray(wordsIndex.files_count)
    initialised = False
    currentBits = BitArray(wordsIndex.files_count)
    negate = False
    state = ''

    iterator = enumerate(expr)
    for i, token in iterator:
        if token == '!':
            negate = True
            continue
        if re.match(OPERATORS, token):
            state = token
            continue

        if token == '(':
            closing_index = i + find_closing_paranthesis(expr[i:])
            # Evaluate the expression between the parantheses
            currentBits = evaluate_expr(
                expr[i + 1:closing_index], wordsIndex).copy()
            # Jump with the iterator after the closing parantheses
            consume(iterator, closing_index - i)

        if is_word(token):
            if token in wordsIndex:
                currentBits = wordsIndex[token].copy()
            # Just ignore the stopwords
            elif token in STOPWORDS:
                negate = False
                currentBits = result.copy()
            else:
                # No match for the current word; Make all the bits 0
                currentBits = BitArray(wordsIndex.files_count)

        result = apply_operator(result, currentBits, negate, state)
        negate = False
        state = None

    return result


def solve_query(query, wordsIndex):
    """Return a BitArray that represents the files that match the query"""

    query = query.lower()
    # Break the query into a list of strings/tokens
    tokens = token_split(query)
    result = evaluate_expr(tokens, wordsIndex)

    return result


def search(query, wordsIndex):
    """Call this function to perform a search in a directory indexed by wordsIndex"""
    # Get the BitArray that indicates the files that apply to the query
    bitsResult = solve_query(query, wordsIndex)

    # Get a list of the name of the files
    files = wordsIndex.get_files(bitsResult)

    return files


if __name__ == '__main__':
    wordsIndex = load_words_index_from_directory('example_docs')
    query = '(linus)||(kernel && runs && programming)'
    output = search(query, wordsIndex)
    print(output)
