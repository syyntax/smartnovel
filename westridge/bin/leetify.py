from random import randint

char_set = {'a': '4', 'e': '3', 'g': '9', 'i': '1', 'l': '1', 'o': '0', \
    's': '5', 't': '7'}


def leetify(n, m):

    # Usage leetify(n, m) where n is the word to leetify and m are the odds
    # (1 of m) that a character will be
    # substituted.

    new_word = ''

    for i in n:
        odds = randint(0, int(m))
        if odds == 1:
            if char_set.get(i.lower()) is not None:
                new_word += str(i).replace(i, char_set[i.lower()])

            else:
                new_word += str(i)

        else:
            new_word += str(i)

    return new_word