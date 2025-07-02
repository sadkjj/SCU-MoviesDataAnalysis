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
        """按预算区间分析票房
        year: 筛选年份，all或不传表示所有年份
        genre_id: 筛选类型，all或不传表示所有类型
    返回:
        List[dict]: 每个预算区间的统计结果，包含:
            - budget_range: 预算区间名称
            - avg_box_office: 平均票房(万元)
            - max_box_office: 最高票房(万元)
            - count: 电影数量
        """
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

        # 使用Spark SQL的CASE WHEN实现区间统计，避免多次扫描数据
        case_expr = "CASE "
        for i, (name, (lower, upper)) in enumerate(budget_ranges):
            if upper == float("inf"):
                case_expr += f"WHEN budget >= {lower} THEN {i} "
            else:
                case_expr += f"WHEN budget >= {lower} AND budget < {upper} THEN {i} "
        case_expr += "ELSE NULL END as budget_range_idx"

        # 注册临时视图
        df.createOrReplaceTempView("movies_stats")

        # 执行聚合查询
        result_df = self.spark.sql(f"""
            SELECT 
                budget_range_idx,
                COUNT(*) as count,
                AVG(total_box_office) as avg_box_office,
                MAX(total_box_office) as max_box_office
            FROM (
                SELECT *, {case_expr}
                FROM movies_stats
                WHERE total_box_office IS NOT NULL
            ) 
            WHERE budget_range_idx IS NOT NULL
            GROUP BY budget_range_idx
        """)

        # 转换为最终结果格式
        results = []
        for row in result_df.collect():
            range_idx = row["budget_range_idx"]
            if 0 <= range_idx < len(budget_ranges):
                range_name = budget_ranges[int(range_idx)][0]
                results.append({
                    "budget_range": range_name,
                    "avg_box_office": round(row["avg_box_office"] / 10000, 2),
                    "max_box_office": round(row["max_box_office"] / 10000, 2),
                    "count": row["count"]
                })

        # 按预算区间顺序排序
        results.sort(key=lambda x: budget_ranges[[r[0] for r in budget_ranges].index(x["budget_range"])])
        return results
