import mapper.Mapper as Mapper


class TimeSpaceAnalysisMapper(Mapper.Mapper):
    def __init__(self):
        super().__init__()

    def get_movie_boxoffices(self, name: str) -> dict:
        query = """(
            SELECT date_time, box_office FROM daily_box_office
            WHERE movie_id = (
                SELECT movie_id FROM movies
                WHERE movies.title = '{}'
            )
        ) AS subquery
        """.format(name)

        df = super().read_table(query).toPandas()

        return {
            "movie": name,
            "status": not df.empty,
            "times": df['date_time'].values.tolist(),
            "box_offices": [float(x) for x in df['box_office']],
        }

    def get_area_data(self, year: int) -> list:
        query = """(
            SELECT m.country, categories.name, COUNT(*) AS count FROM movie_categories
            JOIN (
                SELECT movie_id, country FROM movies
                WHERE release_date LIKE '{}%'
            ) AS m ON m.movie_id = movie_categories.movie_id
            JOIN categories ON categories.genre_id = movie_categories.genre_id
            GROUP BY m.country, categories.name
        ) AS subquery
        """.format(year)

        df = super().read_table(query).toPandas()
        area_data = []
        last_country = ""

        i = 0
        while i < len(df):
            if df.at[i, "country"] != last_country:
                area_data.append({})
                last_country = df.at[i, "country"]
                area_data[-1]["area"] = last_country
                area_data[-1]["type_data"] = []

            area_data[-1]["type_data"].append({
                "type": df.at[i, "name"],
                "count": int(df.at[i, "count"]),
            })

            i = i + 1

        return area_data
