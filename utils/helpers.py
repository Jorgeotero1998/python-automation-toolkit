import random
import time

def random_sleep(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

def scroll_down_human(page):
    for i in range(random.randint(3, 6)):
        page.mouse.wheel(0, random.randint(300, 700))
        random_sleep(0.5, 1.5)
