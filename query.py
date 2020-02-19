from bitstring import BitArray
from loader import load_words_index
import re

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
        token = re.split(DELIMITERS, token)
        # Remove empty strings from list
        token = list(filter(None, token))
        tokens.extend(token)

    return tokens


def is_word(s):
    return not re.match(DELIMITERS, s)

def find_closing_paranthesis(tokens):
    """Return index of the closing paranthesis"""
    depth = 0

    for index, token in enumerate(tokens):
        if token == '(':
            depth += 1
        elif token == ')':
            epth -= 1
        if depth == 0:
            return index
    
    return len(tokens)

def evaluate_expr(expr, wordsIndex):
    """Evaluate the expression using the logical 
        operations from BitArray
    """
    result = BitArray()

    previousBits = BitArray()
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
            closing_index = find_closing_paranthesis(tokens[i:])
            currentBits = evaluate_expr(tokens[i:j])
            # TODO Jump iterator to after the closing parathesis 

        if is_word(token):
            if token in wordsIndex:
                currentBits = wordsIndex[token]
            else:
                currentBits = BitArray()

        if negate:
            currentBits = ~currentBits
            negate = False

        if state == '&&':
            result &= currentBits
        elif state == '||':
            result |= currentBits

    return result


def solve_query(query, wordsIndex):
    """Return a list of files that match the query"""

    query = query.lower()
    tokens = token_split(query)
    result = evaluate_expr(tokens, wordsIndex)

    return result


if __name__ == '__main__':
    wordsIndex = load_words_index('example_docs')
    query = 'Linus   || Torvalds   &&kernel && C || ((!cat &&bread) && !dog)'
    solve_query(query, wordsIndex)
