import random
import sys

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

with open('sevenletterwords.txt') as word_list_file:
    WORDS = [word.strip().upper() for word in word_list_file.readlines()]


class HackingMinigame:
    def __init__(self):
        self.game_words = self.get_words()
        self.computer_memory = self.get_computer_memory_string(self.game_words)
        self.secret_password = random.choice(self.game_words)

    def run(self):
        print('''
Hacking Minigame

Find the password in the computer's memory. You are given clues after
each guess. For example, if the secret password is MONITOR but the
player guessed CONTAIN, they are given the hint that 2 out of 7 letters
were correct, because both MONITOR and CONTAIN have the letter O and N
as their 2nd and 3rd letter. You get four guesses.\n''')
        input('Press Enter to begin...')

        print(self.computer_memory)
        for tries_remaining in range(4, 0, -1):
            player_move = self.ask_for_player_guess(
                self.game_words, tries_remaining)
            if player_move == self.secret_password:
                print('A C C E S S   G R A N T E D')
                return
            else:
                num_matches = self.num_matching_letters(
                    self.secret_password, player_move)
                print(f'Access Denied ({num_matches}/7 correct)')
        print(f'Out of tries. Secret password was {self.secret_password}.')

    @staticmethod
    def get_words():
        secret_password = random.choice(WORDS)
        words = [secret_password]

        while len(words) < 3:
            random_word = HackingMinigame.get_one_word_except(words)
            if HackingMinigame.num_matching_letters(secret_password, random_word) == 0:
                words.append(random_word)

        for _ in range(500):
            if len(words) == 5:
                break

            random_word = HackingMinigame.get_one_word_except(words)
            if HackingMinigame.num_matching_letters(secret_password, random_word) == 3:
                words.append(random_word)

        for _ in range(500):
            if len(words) == 12:
                break

            random_word = HackingMinigame.get_one_word_except(words)
            if HackingMinigame.num_matching_letters(secret_password, random_word) != 0:
                words.append(random_word)

        while len(words) < 12:
            random_word = HackingMinigame.get_one_word_except(words)
            words.append(random_word)

        assert len(words) == 12
        return words

    @staticmethod
    def get_one_word_except(blocklist=None):
        if blocklist is None:
            blocklist = []

        while True:
            random_word = random.choice(WORDS)
            if random_word not in blocklist:
                return random_word

    @staticmethod
    def num_matching_letters(word1, word2):
        return sum(1 for letter1, letter2 in zip(word1, word2) if letter1 == letter2)

    @staticmethod
    def get_computer_memory_string(words):
        lines_with_words = random.sample(range(16 * 2), len(words))
        memory_address = 16 * random.randint(0, 4000)
        computer_memory = []

        next_word = 0
        for line_num in range(16):
            left_half, right_half = '', ''

            for _ in range(16):
                left_half += random.choice(GARBAGE_CHARS)
                right_half += random.choice(GARBAGE_CHARS)

            if line_num in lines_with_words:
                insertion_index = random.randint(0, 9)
                left_half = left_half[:insertion_index] + \
                    words[next_word] + left_half[insertion_index + 7:]
                next_word += 1

            if line_num + 16 in lines_with_words:
                insertion_index = random.randint(0, 9)
                right_half = right_half[:insertion_index] + \
                    words[next_word] + right_half[insertion_index + 7:]
                next_word += 1

            computer_memory.append(
                f'0x{memory_address:04X}  {left_half}    0x{memory_address + (16*16):04X}  {right_half}')
            memory_address += 16

        return '\n'.join(computer_memory)

    @staticmethod
    def ask_for_player_guess(words, tries):
        while True:
            print(f'Enter password: ({tries} tries remaining)')
            guess = input('> ').upper()
            if guess in words:
                return guess
            print(f'That is not one of the possible passwords listed above.')
            print(f'Try entering "{words[0]}" or "{words[1]}".')


if __name__ == '__main__':
    try:
        hacking_game = HackingMinigame()
        hacking_game.run()
    except KeyboardInterrupt:
        sys.exit()
