from typing import Dict
import random
import json

with open('data/word_freq.json') as f:
    word_freq = json.loads(f.read())

class Wordle:
    # dl = disallowed_letters, rp=right_place, rp=wrong_place
    def __init__(
        self,
        dl=None,
        rp=None,
        wp=None,
        possible_words=None,
        input: list[Dict]=None,
    ):
        if dl is None:
            self.dl = list()
        if rp is None:
            self.rp: Dict[int, str] = dict()
        if wp is None:
            self.wp: Dict[int, str] = dict()
        if input is None:
            self.input = list()
        if possible_words is None:
            self.possible_words = self._get_word_list()

        self.possible_words_len = len(self.possible_words)

    # def get_good_word_picks(self):
    #     self.good_word_picks = [
    #         word for word in self.possible_words if len(set(word)) == 5
    #     ]

    def _get_word_list(self):
        with open("/usr/share/dict/words") as f:
            word_list = [line.rstrip("\n") for line in f]

        word_list = list(set([word.lower() for word in word_list])) # turn all words lowercase and remove dupes
        word_list = [word for word in word_list if len(word) == 5] # only look at 5 letter words
        word_list.sort() # sort alphabetically
        return word_list

    @staticmethod
    def any_letters_in_word(letters: str, word: str) -> bool:
        """
        check to see if any letter in a string are in a word.
        any_letters_in_word('gkt','kerb') return True, since k is in kerb
        """
        letters_bool = [i in word for i in letters]
        return any(letters_bool)

    def get_user_input(self):
        """
        Asks for a users word and colors and the formats into a dictionary.
        Places into the input list
        """
        input_dict = dict()
        word = input("Type your last word guess: ")

        if len(word)!=5:
            raise Exception("Word must be 5 letters")
        colors = input("Type the colors of the letters: ")
        if len(colors)!=5:
            raise Exception("There must be exactly 5 colors")

        for x,i in enumerate(tuple(zip(word,colors) ) ):
            input_dict[x] = dict( [ ('letter',i[0]),('color',i[1] ) ] )
        
        self.input.append(input_dict)

        return None

    def print_words_examples(self,n=5)->None:
        print("\n### EXAMPLE WORDS ###")
        try:
            print(random.sample(self.possible_words,min(len(self.possible_words),n)))
        except ValueError as e:
            print('There are less that 5 examples, showing 1 example')


    def print_best_picks(self,n=5)->None:
      
        print("\n### BEST PICK WORDS ###")
        no_dupe_letters= [word for word in self.possible_words if len(''.join(set(word)))==5  ]
        word_with_freq = [( w, self.freq_score(w) ) for w in no_dupe_letters]
        word_with_freq.sort(key=lambda x:-x[1])
        # max_freq= max(word_with_freq,key = lambda x:x[1])[1] 
        best_picks = [ w[0] for w in word_with_freq[0:min(5,len(word_with_freq))]  ]
        print(", ".join(best_picks))


    def print_current_state(self)->None:
        word_perc = round(100* (len(self.possible_words) / self.possible_words_len),3)
        print(f"""\n### CURRENT STATE ###\n{len(self.possible_words)} / {self.possible_words_len} words available ({word_perc }%).\n### CURRENT STATE ###"""     
        )
        return None
    
    @staticmethod
    def freq_score(word):
        return sum([word_freq[letter] for letter in word])



    def dl_rule(self):
        """Using the disallowed letters input to change the state of possible words"""
        self.possible_words = [word for word in self.possible_words if not self.any_letters_in_word(self.dl, word) ]
        return None

    def rp_rule(self)->None:
        """Using right place letters input to change the state of possible words"""
        for i in self.rp:
            self.possible_words = [word for word in self.possible_words if word[i] == self.rp[i]]
        return None

    def wp_check(self, word, n):
        """Check if the word has the letter in the position of the wrong place letter"""
        # print(self.wp)
        check = (word[n] != self.wp[n]) and (self.wp[n] in word)
        return check

    def wp_rule(self)->None:
        """Using right place letters input to change the state of possible words"""
        for i in self.wp:
            self.possible_words = [word for word in self.possible_words if self.wp_check(word,i) ] #check that the word does have the letter in the position we know its not in
            self.possible_words = [word for word in self.possible_words if self.wp[i] in word] # check that the letter is indeed in the word
        return None

    def update_possible_words(self)->None:
        self.dl_rule()
        self.rp_rule()
        self.wp_rule()
        return None

    def check_letter_in_other_categories(self,cats_to_check:list)-> bool:
        return False

    def parse_input(self, input):
        for i in input:

            if input[i]["color"] == "b":
                self.dl.append(input[i]["letter"])    

            if input[i]["color"] == "g":
                self.rp[i] = input[i]["letter"]

            if input[i]["color"] == "y":
                self.wp[i] = input[i]["letter"]

def main():
    w = Wordle()
    while True:
        w.get_user_input()
        w.parse_input(w.input[-1]) #parse the most recent input
        w.update_possible_words() #update the state
        w.print_current_state()
        w.print_words_examples(n= 5)
        w.print_best_picks(n= 3)



if __name__ == "__main__":
    main()



