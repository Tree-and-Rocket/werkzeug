import os


def rreplace(s, old, new, occurrence=1):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def ensure_dirs(dir_in):
    if not os.path.exists(dir_in):
        os.makedirs(dir_in)
 

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


 def int_to_base(number, chars=None):
    if not chars:
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    chars_length = len(chars)
    if number < 0:
        raise Exception("Only positive values and 0 are supported for int_to_base conversion")
    result = ''
    while number:
        result += chars[number % chars_length]
        number //= chars_length
    # [::-1] reverses the number "4321" --> "1234"
    return result[::-1]
