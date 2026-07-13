# Generate and plot prime distribution on Casio fx-CG100.

from matplotlib.pyplot import axis, plot, show
import math

try:
    from casioplot import getkey
except ImportError:
    getkey = None


def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i in range(2, n + 1) if is_p[i]]


def wait_for_exit():
    if getkey is not None:
        getkey()
    else:
        input("\nPress EXE to exit: ")


def main():
    N = 250
    primes = sieve(N)
    
    print("Total Primes:", len(primes))
    print("Max Prime:", primes[-1])

    axis([0, N, 0, len(primes) + 2])

    plot_local = plot
    current_count = 0
    prev_x = 0

    for p in primes:
        plot_local([prev_x, p], [current_count, current_count])
        current_count += 1
        plot_local([p, p], [current_count - 1, current_count])
        prev_x = p

    plot_local([prev_x, N], [current_count, current_count])

    show()
    wait_for_exit()


main()
