from bitstring import BitArray

def solve_query(query):
    """Return a list of files that match the query"""
    result = BitArray()
    query = query.lower()
    query = query.split(' ')

if __name__ == '__main__':
    solve_query('Linus || Torvalds && kernel && C || cat && !dog')