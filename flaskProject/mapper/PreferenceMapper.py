import flaskProject.mapper.Mapper as Mapper


class PreferenceAnalysisMapper(Mapper.Mapper):
    def __init__(self):
        super().__init__()

    def get_audience_preference(self, movie_type: str, start_month: str, end_month: str) -> dict:
        query = """(
            SELECT month_date, SUM(attendees) AS attendees FROM movie_time
            WHERE movie_id IN (
                SELECT movie_id FROM movie_categories
                WHERE genre_id = (
                    SELECT genre_id FROM categories
                    WHERE name = '{}'
                )
            )
            AND month_date >= '{}'
            AND month_date <= '{}'
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
            SELECT * FROM month_data
            WHERE month_date >= '{}' AND month_date <= '{}'
        ) AS subquery
        """.format(start_month, end_month)

        df = super().read_table(query).toPandas()

        return {
            "times": df['month_date'].tolist(),
            "ticket_prices": [float(x) for x in df['ticket_price']],
            "box_offices": [float(x) for x in df['box_office']],
        }
