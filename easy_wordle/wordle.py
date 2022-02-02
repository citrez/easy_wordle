from typing import Dict
import random

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

        # if input is None:
        #     self.input = input

        if possible_words is None:
            self.possible_words = self._get_word_list()

        self.possible_words_len = len(self.possible_words)

        # self.test_input = {
        #     0: {"letter": "a", "color": "b"},
        #     1: {"letter": "u", "color": "b"},
        #     2: {"letter": "d", "color": "b"},
        #     3: {"letter": "i", "color": "b"},
        #     4: {"letter": "g", "color": "b"},
        # }

        # self.test_input2 = {
        #     0: {"letter": "f", "color": "b"},
        #     1: {"letter": "a", "color": "b"},
        #     2: {"letter": "d", "color": "b"},
        #     3: {"letter": "i", "color": "b"},
        #     4: {"letter": "y", "color": "g"},
        # }

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
        check to see if any letter in a string are in a word
        any_letters_in_word('gkt','kerb') return True, since k is in kerb
        """
        letters_bool = [i in word for i in letters]
        return any(letters_bool)

    def get_user_input(self):
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

    def print_possible_words_examples(self,n=5)->None:
        print(random.sample(self.possible_words,n))

    def print_current_state(self)->None:
        print(f"""
### CURRENT STATE ###

{len(self.possible_words)} / {self.possible_words_len} words available ({ round(100* (len(self.possible_words) / self.possible_words_len),3) }%).\n
Possible example words: {w.print_possible_words_examples()}
### CURRENT STATE ###
             """     
        )
        return None

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
        print(cats_to_check)
        return False

    def parse_input(self, input):
        for i in input:
            if input[i]["color"] == "b":
                if self.check_letter_in_other_categories(cats_to_check=['g','y']):
                    raise Exception

                elif not (input[i]["letter"] in self.dl):
                    self.dl.append(input[i]["letter"])    

            if input[i]["color"] == "g":
                self.rp[i] = input[i]["letter"]

            if input[i]["color"] == "y":
                self.wp[i] = input[i]["letter"]


if __name__ == "__main__":
    w = Wordle()

    while True:
        w.get_user_input()
        w.parse_input(w.input[-1])
        w.update_possible_words()
        w.print_current_state()



