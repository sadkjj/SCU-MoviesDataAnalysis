from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc
from flaskProject.config import Config
import json


class TeamAnalysisMapper:
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()
        self.url = Config.MYSQL_URL
        self.user = Config.MYSQL_USER
        self.password = Config.MYSQL_PASSWORD
        self.driver = Config.MYSQL_DRIVER
        self.movie_table = "movies"  # 假设电影数据表名
        self.director_table = "directors"  # 导演表
        self.actor_table = "actors"

    def get_director_boxoffice_ranking(self, start_year=None, end_year=None, top_n=10):
        """
        获取导演票房排行榜
        :param start_year: 开始年份(int)
        :param end_year: 结束年份(int)
        :param top_n: 返回前N名导演(int)
        :return: {
            "ranking": [
                {
                    "rank": 1,
                    "name": "王晶",
                    "totalMovies": 35,
                    "totalBoxOffice": 205.5  # 单位：万元
                },
                ...
            ]
        }
        """
        # 构建基础查询（关联movies和movie_directors表）
        query = """
            (SELECT 
                d.director_id,
                d.name,
                COUNT(m.movie_id) AS movie_count,
                SUM(m.total_box_office) AS total_boxoffice
            FROM directors d
            JOIN movie_directors md ON d.director_id = md.director_id
            JOIN movies m ON md.movie_id = m.movie_id
            WHERE m.total_box_office IS NOT NULL
        """

        # 添加年份筛选条件
        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) <= {end_year}")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += f" GROUP BY d.director_id, d.name ORDER BY total_boxoffice DESC LIMIT {top_n}) AS director_ranking"

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        # 转换为所需格式并添加排名
        results = []
        for index, row in enumerate(df.collect(), start=1):
            results.append({
                "rank": index,
                "name": row["name"],
                "totalMovies": int(row["movie_count"]),
                "totalBoxOffice": float(row["total_boxoffice"]) if row["total_boxoffice"] else 0.0
            })

        return {"ranking": results}

    def get_top_directors(self, start_year=None, end_year=None, top_n=10):
        """
        获取前N名导演的评分统计和电影信息
        :param start_year: 开始年份(可选)
        :param end_year: 结束年份(可选)
        :param top_n: 返回前N名导演(默认10)
        :return: [
            {
                "director": "导演姓名",
                "averageRating": 平均分,
                "movies": ["电影1", "电影2", ...]
            },
            ...
        ]
        """
        # 构建基础查询
        query = """
            (SELECT 
                d.name AS director,
                AVG(m.overall_rating) AS avg_rating,
                GROUP_CONCAT(DISTINCT m.title ORDER BY m.release_date DESC SEPARATOR '|') AS movie_titles
            FROM directors d
            JOIN movie_directors md ON d.director_id = md.director_id
            JOIN movies m ON md.movie_id = m.movie_id
            WHERE m.overall_rating IS NOT NULL
        """

        # 添加年份筛选条件
        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) <= {end_year}")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += f"""
            GROUP BY d.director_id, d.name
            HAVING COUNT(m.movie_id) >= 1
            ORDER BY avg_rating DESC
            LIMIT {top_n}
        ) AS top_directors
        """

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        # 处理结果
        results = []
        for row in df.collect():
            # 将电影名称字符串拆分为列表
            movies = row["movie_titles"].split("|") if row["movie_titles"] else []

            results.append({
                "name": row["director"],
                "averageRating": round(float(row["avg_rating"]), 1),
                "movies": movies
            })

        return results

    def get_director_genre_stats(self, director_name, start_year=None, end_year=None):
        """
        获取导演类型偏好统计
        :param director_name: 导演姓名(必填)
        :param start_year: 开始年份(可选)
        :param end_year: 结束年份(可选)
        :return: {
            "director": "导演姓名",
            "totalMovies": 总电影数,
            "genreCounts": [
                {
                    "genre": "类型名称",
                    "count": 数量
                },
                ...
            ]
        }
        """
        # 构建基础查询（四表关联）
        query = """
               (SELECT 
                   d.name AS director,
                   c.name AS genre,
                   COUNT(m.movie_id) AS count
               FROM directors d
               JOIN movie_directors md ON d.director_id = md.director_id
               JOIN movies m ON md.movie_id = m.movie_id
               JOIN movie_categories mc ON m.movie_id = mc.movie_id
               JOIN categories c ON mc.genre_id = c.genre_id
               WHERE d.name = '{}'
           """.format(director_name)

        # 添加年份筛选条件
        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) <= {end_year}")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY d.director_id, d.name, c.genre_id, c.name) AS director_genres"

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        # 计算总电影数
        total_movies = df.agg({"count": "sum"}).collect()[0][0] or 0

        # 转换为所需格式并按数量降序排列
        genre_counts = df.orderBy(desc("count")) \
            .select("genre", "count") \
            .collect()

        return {
            "director": director_name,
            "totalMovies": int(total_movies),
            "genreCounts": [{
                "genre": row["genre"],
                "count": int(row["count"])
            } for row in genre_counts]
        }

    def get_actor_stats(self,  start_year=None, end_year=None,actor_name=None):
        """
        获取演员统计信息
        :param actor_name: 演员姓名(必填)
        :param start_year: 开始年份(可选)
        :param end_year: 结束年份(可选)
        :return: {
            "actor": "演员姓名",
            "totalMovies": 总电影数,
            "overallRating": {
                "average": 平均评分
            },
            "genreStats": [
                {
                    "genre": "类型名称",
                    "count": 数量,
                    "averageRating": 类型平均分
                },
                ...
            ]
        }
        """
        # 构建基础查询（四表关联）
        query = """
               (SELECT 
                   a.name AS actor,
                   c.name AS genre,
                   m.overall_rating,
                   COUNT(m.movie_id) OVER (PARTITION BY a.actor_id) AS total_movies,
                   AVG(m.overall_rating) OVER (PARTITION BY a.actor_id) AS overall_avg
               FROM actors a
               JOIN movie_actors ma ON a.actor_id = ma.actor_id
               JOIN movies m ON ma.movie_id = m.movie_id
               JOIN movie_categories mc ON m.movie_id = mc.movie_id
               JOIN categories c ON mc.genre_id = c.genre_id
               WHERE a.name = '{}' AND m.overall_rating IS NOT NULL
           """.format(actor_name)

        # 添加年份筛选条件
        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) <= {end_year}")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += ") AS actor_data"

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()
        first_row = df.first()
        total_movies = first_row["total_movies"]
        overall_avg = first_row["overall_avg"]

        # 获取类型统计信息
        genre_stats_df = df.groupBy("genre").agg(
            count("overall_rating").alias("count"),
            avg("overall_rating").alias("averageRating")
        ).orderBy(desc("count"))

        # 转换为所需格式
        return {
            "actor": actor_name,
            "totalMovies": int(total_movies),
            "overallRating": {
                "average": round(float(overall_avg), 1)
            },
            "genreStats": [{
                "genre": row["genre"],
                "count": int(row["count"]),
                "averageRating": round(float(row["averageRating"]), 1)
            } for row in genre_stats_df.collect()]
        }