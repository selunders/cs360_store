import random

def randomPhoto():
    randInt = random.randint(10000,99999)
    return f'https://picsum.photos/400/300?random={randInt}'