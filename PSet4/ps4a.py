# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # I know there is another way this task should be done (I looked in the Internet)
    # but this one is what I came up with based on my thinking only
    if len(sequence) == 1:
        return [sequence]
    result = []
    prev_result = get_permutations(sequence[:-1])
    for i in prev_result:
        tmp = add_letter_to_str(i, sequence[-1])
        for _t in tmp:
            if _t not in result:
                result.append(_t)
    return result


def add_letter_to_str(sequence, letter):
    res = []
    for i in range(len(sequence)+1):
        _s = sequence[0:i] + letter + sequence[i:]
        res.append(_s)
    return res

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))
    
   example_input = 'abcd'
   print('Input:', example_input)
   print('Expected Output:', ['abcd', 'abdc', 'acbd', 'acdb', 'adbc', 'adcb', 'bacd', 'badc', 'bcad', 'bcda', 'bdac', 'bdca', 'cabd', 'cadb', 'cbad', 'cbda', 'cdab', 'cdba', 'dabc', 'dacb', 'dbac', 'dbca', 'dcab', 'dcba'])
   print('Actual Output:', get_permutations(example_input))

   example_input = 'fafa'
   print('Input:', example_input)
   print('Expected Output:', ['fafa', 'faaf', 'ffaa', 'ffaa', 'faaf', 'fafa', 'affa', 'afaf', 'affa', 'afaf', 'aaff', 'aaff', 'ffaa', 'ffaa', 'fafa', 'faaf', 'fafa', 'faaf', 'afaf', 'affa', 'aaff', 'aaff', 'affa', 'afaf'])
   print('Actual Output:', get_permutations(example_input))