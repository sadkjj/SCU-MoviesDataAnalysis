import mapper.Mapper as Mapper


class PreferenceAnalysisMapper(Mapper.Mapper):
    def __init__(self):
        super().__init__()

    def get_audience_preference(self, movie_type: str, start_month: str, end_month: str) -> dict:
        query = """(
            SELECT DATE_FORMAT(date_time, '%Y-%m') as month_date, SUM(attendees) AS attendees FROM daily_box_office
            WHERE movie_id IN (
                SELECT movie_id FROM movie_categories
                WHERE genre_id = (
                    SELECT genre_id FROM categories
                    WHERE name = '{}'
                )
            )
            AND date_time >= '{}'
            AND date_time <= '{}'
            GROUP BY month_date
        ) AS subquery
        """.format(movie_type, start_month, end_month)

        df = super().read_table(query).toPandas()

        return {
            "times": df['month_date'].tolist(),
            "attendees": [int(x) for x in df['attendees']],
        }

    def get_industry_data(self, start_month: str, end_month: str) -> dict:
        query = """(
            SELECT DATE_FORMAT(date_time, '%Y-%m') as month_date, SUM(box_office) as sum FROM daily_box_office
            WHERE date_time >= '{}' AND date_time <= '{}'
            GROUP BY month_date
        ) AS subquery
        """.format(start_month, end_month)

        df = super().read_table(query).toPandas()

        return {
            "times": df['month_date'].tolist(),
            "box_offices": [float(x) for x in df['sum']],
        }
