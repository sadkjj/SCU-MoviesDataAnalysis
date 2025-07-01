from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc
from flaskProject.config import Config


class ContentAnalysisMapper:
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()
        self.url = Config.MYSQL_URL
        self.user = Config.MYSQL_USER
        self.password = Config.MYSQL_PASSWORD
        self.driver = Config.MYSQL_DRIVER
        self.movie_table = "movies"  # 假设电影数据表名
        self.director_table = "directors"  # 导演表
        self.actor_table = "actors"  # 演员表
    def get_movie_type_distribution(self, start_year=None, end_year=None, country=None):
        query = """
            (SELECT 
                c.name as genre,
                COUNT(mc.movie_id) as count
            FROM movie_categories mc
            JOIN categories c ON mc.genre_id = c.genre_id
            JOIN movies m ON mc.movie_id = m.movie_id
        """

        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS INT) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS INT) <= {end_year}")
        if country:
            conditions.append(f"m.country = '{country}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY c.genre_id, c.name) as type_distribution"

        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        total = df.agg({"count": "sum"}).collect()[0][0]
        result = df.withColumn("percentage", col("count") / total * 100) \
                .orderBy(desc("count")) \
                .collect()

        return [row.asDict() for row in result]