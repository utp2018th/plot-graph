import numpy as np
def generate_random_color():
    ans = ""
    while len(ans) != 7:
        ans = '#{:X}{:X}{:X}'.format(*[np.random.randint(0, 255) for _ in range(3)])
    return ans

if __name__ == "__main__":
    for i in range(3):
        print(generate_random_color())
