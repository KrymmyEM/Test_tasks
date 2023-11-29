import random
import string
import logging
async def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return rand_string


def log_info(text):
    logging.log(logging.INFO, text)
