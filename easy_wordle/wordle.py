from typing import Dict

class Wordle:
    # dl = disallowed_letters, rp=right_place, rp=wrong_place
    def __init__(
        self,
        dl=None,
        rp=None,
        wp=None,
        possible_words=None,
        input_dict=None,
    ):
        if dl is None:
            self.dl = list()
        if rp is None:
            self.rp: Dict[int, str] = dict()
        if wp is None:
            self.wp: Dict[int, str] = dict()
        if input_dict is None:
            self.input_dict = dict()

        # if input_dict is None:
        #     self.input_dict = input_dict

        if possible_words is None:
            self.possible_words = self.get_word_list()

        self.test_input = {
            0: {"letter": "a", "color": "b"},
            1: {"letter": "u", "color": "b"},
            2: {"letter": "d", "color": "b"},
            3: {"letter": "i", "color": "b"},
            4: {"letter": "g", "color": "b"},
        }

        self.test_input2 = {
            0: {"letter": "f", "color": "b"},
            1: {"letter": "a", "color": "b"},
            2: {"letter": "d", "color": "b"},
            3: {"letter": "i", "color": "b"},
            4: {"letter": "y", "color": "g"},
        }

    def get_good_word_picks(self):
        self.good_word_picks = [
            word for word in self.possible_words if len(set(word)) == 5
        ]

    def get_word_list(self):
        with open("/usr/share/dict/words") as f:
            word_list = [line.rstrip("\n") for line in f]

        word_list = list(set([word.lower() for word in word_list]))

        word_list = [word for word in word_list if len(word) == 5]
        word_list.sort()

        self.word_list_length = len(word_list)

        return word_list

    @staticmethod
    def any_letters_in_word(letters: str, word: str) -> bool:
        letters_bool = [i in word for i in letters]
        return any(letters_bool)

    def get_user_input(self):
        word = input("Type your last word guess: ")
        colors = input("Type the colors of the letters: ")

        for x,i in enumerate(tuple(zip(word,colors) ) ):
            self.input_dict[x] = dict( [ ('letter',i[0]),('color',i[1] ) ] )
        return None

    def print_possible_words_examples()->None:
        pass

    def print_current_state(self):
        print(f"""
### CURRENT STATE ###

{len(self.possible_words)} / {self.word_list_length} words available ({ round(100* (len(self.possible_words) / self.word_list_length),3) }%).\n
The disallowed letters are {self.dl}.
The correct letters are: {self.rp}
The correct letters, wrong place are: {self.wp}
{w.possible_words[0:5]}
### CURRENT STATE ###
             """     
        )


        return None

    def dl_rule(self):
        # these funcs update state
        self.possible_words = [word for word in self.possible_words if not self.any_letters_in_word(self.dl, word) ]
        return None

    def rp_rule(self)->None:
        # these funcs update state
        updated_possible_words = list()
        for i in self.rp:
            # self.possible_words = [word for word in self.possible_words if word[i] == self.rp[i]]
            for word in self.possible_words:
                if (word[i] == self.rp[i]):
                    print(word)
                    updated_possible_words.append(word)
            self.possible_words = updated_possible_words

        return None

    def wp_rule(self):

        def wp_check(self, word, n):
            check = (word[n] != self.wp[n]["letter"]) and (self.wp[n]["letter"] in word)
            return check

        for i in self.wp:
            self.possible_words = [word for word in self.possible_words if wp_check(word,i) ]
            self.possible_words = [word for word in self.possible_words if self.test_input[i]["letter"] in word]
        return None


    def update_possible_words(self)->None:
        self.dl_rule()
        self.rp_rule()
        return None

   
    def check_letter_in_other_categories(self,cats_to_check:list)-> bool:
        print(cats_to_check)
        return False

    def parse_input_dict(self, input_dict):
        print("Parsing Input:")

        for i in input_dict:

            if input_dict[i]["color"] == "b":
                if self.check_letter_in_other_categories(cats_to_check=['g','y']):
                    raise Exception

                elif not (input_dict[i]["letter"] in self.dl):
                    self.dl.append(input_dict[i]["letter"])    

            if input_dict[i]["color"] == "g":
                self.rp[i] = input_dict[i]["letter"]

            if input_dict[i]["color"] == "y":
                self.wp[i] = input_dict[i]["letter"]


if __name__ == "__main__":
    w = Wordle()

    # print(w.possible_words[0:5])
    # w.print_current_state()
    w.get_user_input()
    print(w.input_dict)

    # w.parse_input_dict(w.test_input)
    # w.update_possible_words()

    # w.print_current_state()

    # w.parse_input_dict(w.test_input2)
    # w.update_possible_words()

    # w.print_current_state()



    # print(w.dl)

    # print(w.good_word_picks[0:5])


