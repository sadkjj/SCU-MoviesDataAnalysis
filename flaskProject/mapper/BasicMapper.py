# mapper/BasicMapper.py
from pyspark.sql import functions as F
from pyspark.sql.window import Window  # 导入窗口函数
from mapper.Mapper import Mapper


class BasicMapper(Mapper):
    def __init__(self):
        super().__init__()

    def get_yearly_movie_count(self, start_year=2021, end_year=2025, country='all'):
        """获取年度电影产量"""
        df = self.read_table("movies")
        df = df.withColumn("year", F.year(F.to_date("release_date")))  # 从日期中提取年份

        # 筛选条件
        if start_year and end_year:
            df = df.filter((F.col("year") >= start_year) & (F.col("year") <= end_year))
        if country and country.lower() != "all":
            df = df.filter(F.lower(F.col("country")) == country.lower())

        return df.groupBy("year").agg(F.count("*").alias("count")) \
            .orderBy("year").collect()  # 按年份分组计数并排序，返回一个List[pyspark.sql.Row]

    def get_monthly_movie_count(self, year):
        """获取月度电影产量"""
        df = self.read_table("movies")
        df = df.withColumn("year", F.year(F.to_date("release_date")))
        df = df.withColumn("month", F.month(F.to_date("release_date")))

        return df.filter(F.col("year") == year) \
            .groupBy("month").agg(F.count("*").alias("count")) \
            .orderBy("month").collect()  # 按月分组计数并排序

    def get_country_movie_stats(self, year=None):
        """获取国家电影产量统计"""
        df = self.read_table("movies")

        if year:
            df = df.withColumn("release_year", F.year(F.to_date("release_date")))
            df = df.filter(F.col("release_year") == year)

        total = df.count()  # 计算总数
        return df.groupBy("country").agg(
            F.count("*").alias("count"),
            (F.count("*") / total * 100).alias("percentage")  # 计算百分比
        ).orderBy(F.col("count").desc()).collect()

    def get_top_movies(self, limit=10, year=None, genre_id=None):
        """获取排名靠前的电影"""
        df = self.read_table("movies")

        # 筛选条件
        if year:
            df = df.withColumn("release_year", F.year(F.to_date("release_date")))
            df = df.filter(F.col("release_year") == year)

        if genre_id:
            movie_categories = self.read_table("movie_categories")
            movie_ids = movie_categories.filter(F.col("genre_id") == genre_id) \
                .select("movie_id").distinct()
            df = df.join(movie_ids, "movie_id")

        # 添加排名
        window = Window.orderBy(F.col("overall_rating").desc())
        df = df.withColumn("rank", F.dense_rank().over(window))

        return df.filter(F.col("rank") <= limit).collect()

    def get_box_office_by_budget(self, year=None, genre_id=None):
        """按预算区间分析票房"""
        df = self.read_table("movies")

        # 筛选条件
        if year and year != "all":
            df = df.withColumn("release_year", F.year(F.to_date("release_date")))
            df = df.filter(F.col("release_year") == year)

        if genre_id and genre_id != "all":
            movie_categories = self.read_table("movie_categories")
            movie_ids = movie_categories.filter(F.col("genre_id") == genre_id) \
                .select("movie_id").distinct()
            df = df.join(movie_ids, "movie_id")

        # 计算预算 (平均票价 * 放映场次)
        df = df.withColumn("budget", F.col("avg_ticket_price") * F.col("screening_count"))

        # 定义预算区间
        budget_ranges = [
            ("<100万", (0, 1000000)),
            ("100-500万", (1000000, 5000000)),
            ("500-1000万", (5000000, 10000000)),
            (">1000万", (10000000, float("inf")))
        ]

        results = []
        for name, (lower, upper) in budget_ranges:
            filtered = df.filter(
                (F.col("total_box_office").isNotNull()) &
                (F.col("budget") >= lower)
            )

            if upper != float("inf"):
                filtered = filtered.filter(F.col("budget") < upper)

            stats = filtered.agg(
                F.avg("total_box_office").alias("avg_box_office"),
                F.max("total_box_office").alias("max_box_office"),
                F.count("*").alias("count")
            ).first()

            if stats["count"] > 0:
                results.append({
                    "budget_range": name,
                    "avg_box_office": round(stats["avg_box_office"] / 10000, 2),
                    "max_box_office": round(stats["max_box_office"] / 10000, 2),
                    "count": stats["count"]
                })

        return results
