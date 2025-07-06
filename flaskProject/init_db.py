from flaskProject.mapper.Mapper import Mapper

ROOT_DIR = "crawler/data/cleaned/"
TARGETS = [
    'actors',
    'directors',
    'categories',
    'movies',
    'movie_actors',
    'movie_categories',
    'movie_directors',
    'daily_box_office',
]

if __name__ == '__main__':
    mapper = Mapper()
    for target in TARGETS:
        table = mapper.spark.read.format('csv').load(ROOT_DIR + target + ".csv", sep=',', header=True, inferSchema=True)
        mapper.write_table(table, target)
