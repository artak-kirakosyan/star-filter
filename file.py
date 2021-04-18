
import os
import math
from typing import Tuple

import config


class Star:
    def __init__(self, star_line: str):
        """
        """
        line = star_line.strip("\n")
        self.line = line
        self.data = self.line.split(config.DB_SEPARATOR)
        try:
            self.ra = float(self.data[config.RA_COLUMN_INDEX])
            self.dec = float(self.data[config.DEC_COLUMN_INDEX])
            self.brightness = float(self.data[config.BRIGHTNESS_COLUMN_INDEX])
        except (ValueError, IndexError) as e:
            print(e)
            print("Failed to create star from %s" % line)
            raise RuntimeError("Invalid star data")

    # def __str__(self):
    #     return self.line + "\n"


class StarFilter:
    def __init__(self, db_location=None):
        if db_location is None:
            db_location = config.DB_FILE_LOCATION
        self.db_location = db_location
        self.check_db_existence()
        self.headers_line = None
        self.headers = []
        self.data = []

        self.load_db()

    def check_db_existence(self):
        if not os.path.isfile(self.db_location):
            raise RuntimeError("DB file does not exist: %s" % self.db_location)

    def load_db(self):
        header_line = True
        with open(self.db_location, "r") as f:
            for line in f:
                line = line.strip("\n")
                if line.startswith("#"):
                    print("Comment line, skipping")
                    continue
                if header_line:
                    self.headers_line = line
                    self.load_headers()
                    header_line = False
                    continue
                try:
                    current_star = Star(line)
                    self.data.append(current_star)
                except RuntimeError:
                    print("Failed to create star from %s, skipping" % line)
        self.data.sort(key=lambda x: x.brightness)
        print("%s stars loaded" % len(self.data))

    def load_headers(self):
        if self.headers_line is None:
            print("Headers line is None, nothing to initialize")
        else:
            self.headers = self.headers_line.split(config.DB_SEPARATOR)
            print("Headers initialized")

    def filter_stars(self, ra: float, dec: float, n: int):
        """
        Get first n brightest stars
         and sort by their distance from the given ra dec
        :param ra: ra of the given point
        :param dec: dec of the given point
        :param n: number of stars to return
        :return: list of stars
        """
        result = self.data[:n]
        result.sort(
            key=lambda x: self.calculate_distance((x.ra, x.dec), (ra, dec))
        )
        distances = []
        for star in result:
            distances.append(
                self.calculate_distance((star.ra, star.dec), (ra, dec)))
        return result, distances

    @staticmethod
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
