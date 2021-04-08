import ulti as ut
import random
import math as ma


class NGramLM():
    def __init__(self, input_list, n):
        self.n = n
        self.all_ngram = ut.get_upto_ngrams(input_list, n)
        self.probability = {}
        for i in range(1, n + 1):
            self.probability[i] = {}
            for word in self.all_ngram[i]:
                ut.calculate_prob(self.all_ngram, word)

    def generate_text(self, length, prompt=[]):
        result = [word for word in prompt]
        while len(result) < length:
            score = random.random()
            # print("Result is: ", result)
            # print("Prompt is: ", prompt)
            if len(prompt) >= self.ngram:
                prompt = prompt[len(prompt) - self.ngram + 1:]
            if tuple(prompt) in self.guess:
                for word, prob in self.guess[tuple(prompt)]:
                    if score < prob:
                        # print("Guess tuple ", word)
                        prompt.append(word)
                        result.append(word)
                        break
                    else:
                        score -= prob
            else:  # len(prompt)
                if len(prompt) == 0:
                    # print("prompt len: ", len(prompt))
                    for word, prob in self.probability[1].items():
                        if score < prob:
                            # print("Prob ", word)
                            prompt.append(word[0])
                            result.append(word[0])
                            break
                        else:
                            score -= prob
                else:
                    if len(prompt) == 1:
                        prompt = []
                    else:
                        prompt = prompt[1:]
        return result

    def score_text(self, text):
        res = 0
        if text == "":
            return 1
        # ['Hamlet','just','use','Google']
        # n = 2
        # using b = 2
        curr = [text[0]]  # [ Hamlet, just ]
        # for j in range(self.ngram - 1, 0, -1):
        i = 1
        while i <= len(text):
            curr_tuple = tuple(curr)
            if len(curr) <= self.ngram:
                if curr_tuple in self.probability[len(curr)]:
                    curr_prob = self.probability[len(curr)][curr_tuple]
                    # print(curr_tuple, curr_prob)
                    res += ma.log2(curr_prob)
                    if i == len(text):
                        break
                    curr.append(text[i])
                    i += 1
                else:
                    if len(curr) < 2:  # This also means that we have looked in unigram
                        return float('inf')
                    else:
                        curr = curr[1:]
            else:
                curr = curr[1:]

        res *= -1 / len(text)
        return 2 ** (res)