import math
from typing import List, Iterator

import config


class Star:
    def __init__(self, star_line: str):
        line = star_line.strip("\n")
        self.line = line
        self.distance = None
        self.data = self.line.split(config.DB_SEPARATOR)
        try:
            self.id = self.data[config.ID_COLUMN_INDEX]
            self.ra = float(self.data[config.RA_COLUMN_INDEX])
            self.dec = float(self.data[config.DEC_COLUMN_INDEX])
            self.brightness = float(self.data[config.BRIGHTNESS_COLUMN_INDEX])
        except (ValueError, IndexError) as e:
            raise RuntimeError("Invalid star data")

    def calculate_distance(self, ra: float, dec: float) -> float:
        """
        Calculate distance from the given point
        :param ra: RA in angles
        :param dec: DEC in angles
        :return: distance from star to given point
        """
        res = (self.ra - ra) ** 2 + (self.dec - dec) ** 2
        res = math.sqrt(res)
        return res

    def set_distance_from_point(self, ra: float, dec: float) -> None:
        """
        Calculate distance from the given point and set it in the self
        :param ra: RA in angles
        :param dec: DEC in angles
        """
        self.distance = self.calculate_distance(ra, dec)

    def to_csv_row(self, separator=config.DB_SEPARATOR):
        data = [self.distance, self.id, self.ra, self.dec, self.brightness]
        str_data = [str(i) for i in data]
        return separator.join(str_data)


class MaxStack:
    """
    This is a data structure that helps keep the most bright n objects
    """
    def __init__(self, max_size: int):
        if max_size < 1:
            raise RuntimeError("Max size cant be smaller than 1")
        self.data: List[Star] = []
        self.min_brightness: float = float("-inf")
        self.max_size: int = max_size

    def __len__(self) -> int:
        return len(self.data)

    def check_star(self, star: Star) -> None:
        """
        Check if the star is brighter than minimum and add into data
        :param star: Star object to check
        :return: None
        """
        if len(self) < self.max_size:
            self.__insert(star)
            return

        if star.brightness < self.min_brightness:
            return
        else:
            self.__insert(star)

    def __insert(self, star: Star) -> None:
        """
        Insert into correct place if needed, otherwise ignore
        :param star: Star object to be inserted
        :return: None
        """
        for i, st in enumerate(self.data):
            if star.brightness > st.brightness:
                self.__push(star, i)
                return
        else:
            self.data.append(star)
            self.__check_overflow()

    def __push(self, star: Star, index: int) -> None:
        """
        Insert a star in the given index
        :param star: Star object
        :param index: the index where to insert the star
        :return: None
        """
        self.data.insert(index, star)
        self.__check_overflow()

    def __check_overflow(self) -> None:
        """
        Check if the storage exceeded max size, then remove the overhead
        Update minimum brightness for future use
        :return:
        """
        while len(self) > self.max_size:
            self.data.pop()
            self.min_brightness = self.data[-1].brightness

    def validate(self) -> None:
        """
        A helper function which checks that the DB is valid(sorted)
        :return: None
        """
        for i in range(len(self) - 1):
            if self.data[i].brightness < self.data[i + 1].brightness:
                print("Invalid")

    def __iter__(self) -> Iterator:
        for star in self.data:
            yield star
