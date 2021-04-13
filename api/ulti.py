from api import search_api as sa


# Get a certain n-gram:
def get_ngrams(input_list, n):
    ngrams = {}
    for i in range(len(input_list) - (n - 1)):
        t = tuple(input_list[i:i + n])
        ngrams[t] = ngrams.get(t, 0) + 1
    return ngrams


# Get up to n-gram:
def get_upto_ngrams(input_list, n):
    ngrams = {}
    for i in range(1, n + 1):
        ngrams[i] = get_ngrams(input_list, i)
    return ngrams


# ngram is all the possible gram
# term is a tuple (A, B),
# len(term) == 1 -> unigram
# len(term) > 1-> has term needs to be calculated B, given term A (A is a tuple):
def calculate_prob(ngram, term):
    if len(term) == 1:
        return ngram[1][term[0]] / (sum(s) for s in ngram[1].values())
    else:
        A = term[:-1]  # n-1 gram
        if len(term) > len(ngram):
            return None
        return ngram[len(term)][term] / ngram[len(A)][A]


if __name__ == "__main__":
    lyrics = sa.get_lyrics("Lady Gaga", 3)
    l = get_anagrams(lyrics, 2)
    print(l)
