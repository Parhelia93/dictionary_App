def check_input_word(input_word):
    alphabet = [chr(i) for i in range(ord('a'), ord('z'))] + [' ']
    for a in input_word.lower():
        if a not in alphabet:
            return True
    return False
