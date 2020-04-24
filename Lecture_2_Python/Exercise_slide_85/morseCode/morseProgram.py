from colorama import init
from termcolor import colored

MORSE_CODE_DICT = {' ': ' ',
                   'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--',
                   '?': '..--..', '/': '-..-.',
                   '(': '-.--.', ')': '-.--.-'}


def message_convert_to_morse_code(message):
    morse_code = ''

    for let in message:
        # the current letter will be appended
        # to the morse_code and seperated by an empty space. The letter is automatically
        # made to upper case in order to properly look it up in the dictonary
        morse_code += MORSE_CODE_DICT[let.upper()]

    return morse_code


def morse_code_convert_to_message(morse_code):
    try:
        message = ''
        morse_code_dict_inverted = dictinvert(MORSE_CODE_DICT)

        for morse in morse_code.split(' '):
            if morse == '':
                message += ''
            elif morse == '#'.strip():
                message += ' '
            else:
                message += morse_code_dict_inverted[morse]

        return message.lower()
    except KeyError:
        return SyntaxError(
            colored("\nERROR IN MORSE: " \
                    "Each letter must be seperated by space and whole words by '#' \n" \
                    "e.g. .... . .--- # .... . .--- will yield 'hej hej' \n", 'red'))


def dictinvert(dic):
    inv_dict = dict(zip(dic.values(), dic.keys()))
    return inv_dict


def main():
    print("Morse code program,")
    msgoption = ''
    run = True
    while (run):
        msgoption = input("\nChoose service by typing 1 or 2. Type 'h' for help. 'q' or 'quit' to exit program: ")
        if (msgoption == '1'):
            msgto = input("Type message to to convert to morse: ")
            msgtoresult = message_convert_to_morse_code(msgto)
            print('Result: ', msgtoresult)
        elif (msgoption == '2'):
            morseto = input("Type morse to to convert to message, seperate letter by space: ")
            morsetoresult = morse_code_convert_to_message(morseto)
            print(morsetoresult)
        elif (msgoption == 'q' or msgoption == 'quit'):
            print("goodbye")
            break;
        elif (msgoption == 'h'):
            print("1: Convert message to morse code \n"
                  "2: Convert morse code to a message")


if __name__ == '__main__':
    init()
    main()
