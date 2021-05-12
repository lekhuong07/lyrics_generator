import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np

import lyricsgenius
from secret_token import TOKEN
from search_api import get_artist, get_lyrics

import ulti as ut
import analysis as ana
from random import randrange
from tqdm import tqdm

'''
#Generate text using Single Layer LSTM Model
class RnnLM():
    def __init__(self, input_list, n):
'''


class RnnLM():
    def __init__(self, input_lyrics, artist_obj):
        self.tokenizer = Tokenizer()
        self.lyr = []

        input_sequences, total_words = self.lstm_index(input_lyrics)
        self.input_sequences = input_sequences
        self.total_words = total_words
        # training features (x) will be a list
        self.max_sequence_len = max([len(x) for x in input_sequences])  # calculating the length of the longest sequence
        self.artist = artist_obj
        # print(self.input_sequences, self.total_words, self.max_sequence_len)

    def lstm_index(self, ll):
        self.lyr = ll
        # print("Lyrics is: ", self.lyr, "len: ", len(self.lyr))
        self.tokenizer.fit_on_texts(ll)
        total_words = len(self.tokenizer.word_index) + 1
        res = []
        for line in ll:
            token_list = self.tokenizer.texts_to_sequences([line])[
                0]  # converts each sentence as its tokenized equivalent
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i + 1]  # generating n gram sequences
                res.append(n_gram_sequence)  # appending each n gram sequence to the list of our features (xs)
        return res, total_words

    def generate_lstm_text(self, model, starter, length):
        for _ in tqdm(range(length)):
            token_list = self.tokenizer.texts_to_sequences([starter])[
                0]  # converting our input_phrase to tokens and excluding the out of vcabulary words
            token_list = pad_sequences([token_list],
                                       maxlen=self.max_sequence_len - 1,
                                       padding='pre')  # padding the input_phrase
            predicted = model.predict_classes(token_list,
                                              verbose=0)  # predicting the token of the next word using our trained model
            output_word = ""  # initialising output word as blank at the beginning
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word  # converting the token back to the corresponding word and storing it in the output_word
                    break
            starter += " " + output_word
        return starter

    def generate_lyrics(self, model):
        # print(self.lyr[randrange(len(self.lyr))], len(self.lyr[randrange(len(self.lyr))]))
        analysis = ana.artist_analysis(self.artist)
        lyrics_starter = ""
        num_words = int(analysis['Chorus'][1])
        num_words += int(analysis['Verse'][1]) * 3
        if analysis['Intro'][0] >= 0.5:
            num_words += int(analysis['Intro'][1])
            lyrics_starter += "[Intro]\n"
        if analysis['Chorus'][0] >= 1.5:
            num_words += int(analysis['Chorus'][1])
        print("Generating ---")
        generated = self.generate_lstm_text(model, self.lyr[randrange(len(self.lyr))], num_words)
        generated = generated.split(" ")
        index = 0
        next_index = 0
        if analysis['Intro'][0] >= 0.5:
            next_index += int(analysis['Intro'][1]) + 1

            intro = generated[:next_index]
            lyrics_starter += ut.list_to_sentence(intro).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Intro'][1]) + 1

        if analysis['Chorus'][0] >= 1.5:
            next_index += int(analysis['Verse'][1]) + 1

            lyrics_starter += "[Verse 1]\n"
            verse1 = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(verse1).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Verse'][1]) + 1

            lyrics_starter += "[Chorus]\n"
            next_index += int(analysis['Chorus'][1]) + 1

            chorus = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(chorus).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1

            lyrics_starter += "[Verse 2]\n"
            next_index += int(analysis['Verse'][1]) + 1

            verse2 = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(verse2).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1

            lyrics_starter += "[Chorus]\n"
            lyrics_starter += ut.list_to_sentence(chorus).capitalize()
            lyrics_starter += "\n"

            lyrics_starter += "[Outro]\n"
            next_index += int(analysis['Verse'][1]) + 1

            outro = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(outro).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1

        else:
            next_index += int(analysis['Verse'][1]) + 1

            lyrics_starter += "[Verse 1]\n"
            verse1 = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(verse1).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Verse'][1]) + 1

            lyrics_starter += "[Chorus]\n"
            next_index += int(analysis['Chorus'][1]) + 1

            chorus = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(chorus).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1

            lyrics_starter += "[Verse 2]\n"
            next_index += int(analysis['Verse'][1]) + 1

            verse2 = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(verse2).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1

            lyrics_starter += "[Outro]\n"
            next_index += int(analysis['Verse'][1]) + 1

            outro = generated[index:next_index]
            lyrics_starter += ut.list_to_sentence(outro).capitalize()
            lyrics_starter += "\n"
            index += int(analysis['Chorus'][1]) + 1
        return lyrics_starter

    def generate_song(self):
        input_sequences = np.array(pad_sequences(self.input_sequences,
                                                 maxlen=self.max_sequence_len,
                                                 padding='pre'))  # pre-pading each value of the input_sequence
        # print(input_sequences, len(input_sequences))
        xs, labels = input_sequences[:, :-1], input_sequences[:, -1]  # creating xs and their labels using numpy slicing
        ys = tf.keras.utils.to_categorical(labels, num_classes=self.total_words)  # creating one hot encoding values

        model = Sequential()  # creating a sequential model
        model.add(Embedding(self.total_words, 64,
                            input_length=self.max_sequence_len - 1))  # adding an embedding layer with 64 as the embedding dimension
        model.add(Bidirectional(LSTM(20)))  # adding 20 LSTM units
        model.add(Dense(self.total_words,
                        activation='softmax'))  # creating a dense layer with 54 output units (total_words) with softmax activation

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])  # compiling the model with adam optimiser

        history = model.fit(xs, ys, epochs=500, verbose=1)  # training for 500 epochs
        result = self.generate_lyrics(model)
        return result


if __name__ == "__main__":
    genius = lyricsgenius.Genius(TOKEN)
    while True:
        try:
            artist = genius.search_artist("Lady Gaga", max_songs=10)
            break
        except:
            pass
    lyrics = get_lyrics(artist)[1]
    # print("Lyrics is:", lyrics)
    lm = RnnLM(lyrics, artist)
    song = lm.generate_song()
    print(song)