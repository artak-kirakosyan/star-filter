import os
import datetime
from typing import Generator

import config

from star import Star, MaxStack


def iterate_over_db(
        db_location: str = config.DB_FILE_LOCATION
) -> Generator[Star, None, None]:
    """
    Generator
    Iterate over the lines of the database and return Star object for each
    :param db_location: location of the file
    :return: Star object per line of the file
    """
    with open(db_location, "r") as f:
        for line in f:
            line = line.strip("\n")
            if line.startswith("#"):
                print("Comment line, skipping")
                continue
            try:
                current_star = Star(line)
                yield current_star
            except RuntimeError:
                print("Failed to create star from %s, skipping" % line)
                continue


def iterate_over_window_stars(
        ra: float,
        dec: float,
        fov_ra: float,
        fov_dec: float,
        db_location: str = config.DB_FILE_LOCATION,
) -> Generator[Star, None, None]:
    for star in iterate_over_db(db_location):
        if check_star_in_window(star, fov_ra, fov_dec, ra, dec):
            yield star
    pass


def calculate_distances(container: MaxStack, ra: float, dec: float) -> MaxStack:
    """
    Calculate distances of the given stars
    :param container: MaxStack object which contains stars
    :param ra: ra of the given point
    :param dec: dec of the given point
    :return: the same container, but added distances
    """
    for star in container.data:
        star.set_distance_from_point(ra, dec)
    return container


def check_star_in_window(star: Star, fov_ra, fov_dec, ra, dec) -> bool:
    """
    Return true if the star is withing given angle view, false otherwise
    :param star: Star object
    :param fov_ra: fov ra component
    :param fov_dec: fov dec component
    :param ra: RA of the center point
    :param dec: DEC of the center point
    :return: boolean indicating if the star is withing given angle view or not
    """
    if abs(ra - star.ra) > fov_ra / 2 or abs(dec - star.dec) > fov_dec / 2:
        return False
    return True


def generate_file_name() -> str:
    timestamp = datetime.datetime.now()
    file_name = timestamp.strftime("%Y_%m_%d_%H_%M_%S")
    if config.DB_SEPARATOR == "\t":
        extension = ".tsv"
    elif config.DB_SEPARATOR == ",":
        extension = ".tsv"
    else:
        extension = ""
    file_name += extension
    return os.path.join(config.RESULTS_DIR, file_name)


def dump_stars_from_container(container: MaxStack) -> str:
    """
    If container is not empty, dump results into the file
    :param container: MaxStack object with all the data in it
    :return: File name in which the results are placed
    """
    if len(container) == 0:
        raise RuntimeError("No stars, nothing to dump")
    file_name = generate_file_name()
    headers = ["distance", "id", "ra", "dec", "magnitude"]
    headers = config.DB_SEPARATOR.join(headers)
    with open(file_name, "w") as f:
        f.write(headers)
        f.write("\n")
        for star in container:
            f.write(star.to_csv_row())
            f.write("\n")
    return file_name


def filter_stars(
        ra: float, dec: float, n: int, fov_ra: float, fov_dec: float
) -> MaxStack:
    c = 0
    if n > 1000:
        print("WARNING: getting more than 1000 stars will take too long")
    container = MaxStack(max_size=n)
    for star in iterate_over_window_stars(ra, dec, fov_ra, fov_dec):
        c += 1
        container.check_star(star)

    print("Stars withing given window: %s" % c)
    calculate_distances(container, ra, dec)
    container.data.sort(key=lambda x: x.distance)
    return container


def main():
    container = filter_stars(335., 57., 100, 3, 3)
    try:
        file_name = dump_stars_from_container(container)
        print("Wrote %s stars in %s" % (len(container), file_name))
    except RuntimeError:
        print("No stars found")


if __name__ == '__main__':
    main()
