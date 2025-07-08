from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc,expr
from pyspark.sql.functions import col, lit, when, sum
from config import Config
import json


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
        self.rating_bins = [(0, 3), (3, 6), (6, 7), (7, 8), (8, 9), (9, 10)]

    def get_type_distribution_analysis(self, start_year=None, end_year=None, country=None):
        try:
            # 基础查询模板（使用MySQL 8.0特性）
            base_query = """
                   WITH filtered_movies AS (
                       SELECT m.movie_id 
                       FROM movies m
                       WHERE m.overall_rating IS NOT NULL
                       {date_condition}
                       {country_condition}
                   )
                   SELECT 
                       c.name AS genre,
                       COUNT(DISTINCT fm.movie_id) AS count,
                       ROUND(COUNT(DISTINCT fm.movie_id) * 100.0 / 
                           (SELECT COUNT(DISTINCT movie_id) FROM filtered_movies), 2) AS percentage
                   FROM filtered_movies fm
                   JOIN movie_categories mc ON fm.movie_id = mc.movie_id
                   JOIN categories c ON mc.genre_id = c.genre_id
                   GROUP BY c.genre_id, c.name
                   ORDER BY count DESC
               """

            # 构建条件
            date_condition = ""
            if start_year and end_year:
                date_condition = f"AND YEAR(m.release_date) BETWEEN {start_year} AND {end_year}"
            elif start_year:
                date_condition = f"AND YEAR(m.release_date) >= {start_year}"
            elif end_year:
                date_condition = f"AND YEAR(m.release_date) <= {end_year}"

            country_condition = f"AND m.country = '{country}'" if country else ""

            # 格式化最终查询
            final_query = base_query.format(
                date_condition=date_condition,
                country_condition=country_condition
            )

            # 执行查询（使用query参数）
            df = self.spark.read.format("jdbc") \
                .option("url", self.url) \
                .option("driver", self.driver) \
                .option("query", final_query) \
                .option("user", self.user) \
                .option("password", self.password) \
                .load()

            # 转换为所需格式
            return [row.asDict() for row in df.collect()]

        except Exception as e:
            import traceback
            traceback.print_exc()
            return []

    def get_type_boxoffice_analysis(self, start_year=None, end_year=None):
        """
        获取不同类型电影的票房统计
        :param start_year: 开始年份(int)
        :param end_year: 结束年份(int)
        :return: [
            {
                "type": "科幻",
                "avgBoxOffice": 15.2,  # 单位：万元
                "maxBoxOffice": 56.8,
                "minBoxOffice": 0.3,
                "totalBoxOffice": 320.5
            },
            ...
        ]
        """
        # 构建基础查询
        query = """
               (SELECT 
                   c.name AS type,
                   AVG(m.total_box_office) AS avgBoxOffice,
                   MAX(m.total_box_office) AS maxBoxOffice,
                   MIN(m.total_box_office) AS minBoxOffice,
                   SUM(m.total_box_office) AS totalBoxOffice
               FROM movies m
               JOIN movie_categories mc ON m.movie_id = mc.movie_id
               JOIN categories c ON mc.genre_id = c.genre_id
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

        query += " GROUP BY c.genre_id, c.name) AS type_boxoffice_stats"

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        # 转换为所需的JSON格式并按总票房降序排列
        #同时将票房单位改为万元

        results = df.orderBy(desc("totalBoxOffice")) \
            .select(
            col("type"),
            col("avgBoxOffice").cast("double"),
            col("maxBoxOffice").cast("double"),
            col("minBoxOffice").cast("double"),
            col("totalBoxOffice").cast("double")
        ) \
            .toJSON() \
            .collect()

        # 将JSON字符串转换为Python字典
        return [json.loads(item) for item in results]

    def get_type_rating_analysis(self, start_year=None, end_year=None, country=None):
        """
        获取类型与评分关系分析
        :param start_year: 开始年份(int)
        :param end_year: 结束年份(int)
        :param country: 国家(str)
        :return: {
            "timeRange": "2018-2023",
            "totalMovies": 1850,
            "analysis": [
                {
                    "type": "剧情",
                    "avgRating": 8.2,
                    "medianRating": 8,
                    "ratingDistribution": {
                        "0-3": 2,
                        "3-6": 15,
                        ...
                    }
                },
                ...
            ]
        }
        """
        # 基础查询获取电影数据
        query = """
            (SELECT 
                m.movie_id,
                m.overall_rating,
                c.name AS type,
                m.release_date,
                m.country
            FROM movies m
            JOIN movie_categories mc ON m.movie_id = mc.movie_id
            JOIN categories c ON mc.genre_id = c.genre_id
            WHERE m.overall_rating IS NOT NULL
        """

        conditions = []
        if start_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) >= {start_year}")
        if end_year:
            conditions.append(f"CAST(SUBSTRING(m.release_date, 1, 4) AS SIGNED) <= {end_year}")
        if country:
            conditions.append(f"m.country = '{country}'")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += ") AS movie_ratings"

        # 执行查询
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        # 计算总电影数
        total_movies = df.count()

        # 按类型分组计算统计指标
        result = {
            "timeRange": f"{start_year}-{end_year}" if start_year and end_year else "全部年份",
            "totalMovies": total_movies,
            "analysis": []
        }

        # 对每个类型计算评分分布
        type_df = df.groupBy("type").agg(
            count("movie_id").alias("movie_count"),
            avg("overall_rating").alias("avgRating"),
            expr("percentile_approx(overall_rating, 0.5)").alias("medianRating")
        ).collect()

        for row in type_df:
            type_name = row["type"]
            type_movies = df.filter(col("type") == type_name)

            # 计算评分分布
            distribution = {}
            for bin_min, bin_max in self.rating_bins:
                bin_count = type_movies.filter(
                    (col("overall_rating") >= bin_min) &
                    (col("overall_rating") < bin_max)
                ).count()
                distribution[f"{bin_min}-{bin_max}"] = bin_count

            # 计算9-10分的特殊处理（包含10分）
            bin_count = type_movies.filter(
                (col("overall_rating") >= 9) &
                (col("overall_rating") <= 10)
            ).count()
            distribution["9-10"] = bin_count

            result["analysis"].append({
                "type": type_name,
                "avgRating": round(float(row["avgRating"]), 1),
                "medianRating": round(float(row["medianRating"]), 1),
                "ratingDistribution": distribution
            })

        # 按平均评分降序排列
        result["analysis"].sort(key=lambda x: x["avgRating"], reverse=True)

        return result