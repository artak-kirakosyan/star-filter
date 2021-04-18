from typing import Tuple, List
import time
import math

import config

from file import Star


class MaxStack:
    def __init__(self, max_size: int):
        self.data: List[Star] = []
        self.min_brightness = float("-inf")
        self.max_size = max_size

    def __len__(self):
        return len(self.data)

    def check_star(self, star: Star):
        if len(self) < self.max_size:
            self.__insert(star)
            return

        if star.brightness < self.min_brightness:
            # print("%s < %s, skip" % (star.brightness, self.min_brightness))
            return
        else:
            self.__insert(star)

    def __insert(self, star: Star):
        for i, st in enumerate(self.data):
            if star.brightness > st.brightness:
                self.__push(star, i)
                return
        else:
            self.data.append(star)
            self.__check_overflow()

    def __push(self, star, index):
        self.data.insert(index, star)
        self.__check_overflow()

    def __check_overflow(self):
        while len(self) > self.max_size:
            popped = self.data.pop()
            # print("popped %s" % popped)
            self.min_brightness = self.data[-1].brightness

    def validate(self):
        for i in range(len(self) - 1):
            if self.data[i].brightness < self.data[i + 1].brightness:
                print("Invalid")


def calculate_distance(p1: Tuple, p2: Tuple):
    """
    :param p1: ra, dec
    :param p2: ra, dec
    :return:
    """
    res = 0
    for i, j in zip(p1, p2):
        res += (i - j) ** 2
    return math.sqrt(res)


def calculate_distance_from_star(star: Star, ra, dec):
    return calculate_distance((star.ra, star.dec), (ra, dec))


def iterate_over_db(db_location=config.DB_FILE_LOCATION):
    header_line = True
    with open(db_location, "r") as f:
        for line in f:
            line = line.strip("\n")
            if line.startswith("#"):
                print("Comment line, skipping")
                continue
            if header_line:
                header_line = False
                continue
            try:
                current_star = Star(line)
                yield current_star
            except RuntimeError:
                print("Failed to create star from %s, skipping" % line)


def get_distances(container: MaxStack, ra, dec):
    distances = {}
    for star in container.data:
        distances[star] = calculate_distance_from_star(star, ra, dec)
    return distances


def filter_stars(ra, dec, n):
    c = 0
    container = MaxStack(max_size=n)
    st = time.time()
    for star in iterate_over_db():
        c += 1
        container.check_star(star)
        container.validate()

    print("Stars: %s" % c)
    distances = get_distances(container, ra, dec)
    print(time.time() - st)
    return container, distances


def main():
    filter_stars(23, 45, 1000)
    st = time.time()
    for star in iterate_over_db():
        pass
    print(time.time() - st)
    # for i in range(10):
    #     if i == 11:
    #         print("break")
    #         break
    # else:
    #     print("now")


if __name__ == '__main__':
    main()
