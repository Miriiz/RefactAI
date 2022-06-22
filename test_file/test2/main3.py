def return_random_list(n):
    import random
    return [random.randint(0, 100) for i in range(n)]


def return_random_string(n):
    import random
    return ''.join([chr(random.randint(97, 122)) for i in range(n)])
