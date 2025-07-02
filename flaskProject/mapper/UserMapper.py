# mapper/UserMapper.py
from pyspark.sql import functions as F
from pyspark.sql.window import Window  # 导入窗口函数
from mapper.Mapper import Mapper


class UserMapper(Mapper):
    def __init__(self):
        super().__init__()

    def get_user_by_username(self, username):
        """根据用户名获取用户信息"""
        df = self.read_table("users")
        user = df.filter(F.col("username") == username).first()
        return user.asDict() if user else None  # 将Row对象转为字典或返回None

    def create_user(self, user_data):
        """注册：创建新用户，只能注册普通用户"""
        from pyspark.sql import Row
        new_user = Row(**user_data)  # 将用户数据字典转为Row对象
        df = self.spark.createDataFrame([new_user])  # 创建单行DataFrame
        self.write_table(df, "users")
        return True

    def get_user_by_id(self, user_id):
        """根据ID获取单个用户信息"""
        df = self.read_table("users")
        user = df.filter(F.col("user_id") == user_id).first()
        return user.asDict() if user else None

    def update_user(self, user_id, update_data):
        """更新用户信息"""
        df = self.read_table("users")
        for key, value in update_data.items():
            # 对每个更新字段，使用when条件更新指定user_id的记录
            df = df.withColumn(key,
                               F.when(F.col("user_id") == user_id, value).otherwise(F.col(key)))
        self.write_table(df, "users", mode="overwrite")  # 覆盖模式写回表
        return True

    def get_movie_list(self, page=1, page_size=10, title=None, genre_id=None, director_id=None, min_rating=0,
                       sort_field='title', sort_order=False):
        """
        获取电影列表
        参数:
            page: 页码(从1开始)
            page_size: 每页大小
            title: 电影标题模糊搜索
            genre_id: 按类型筛选
            director_id: 按导演筛选
            min_rating: 最低评分阈值
            sort_field: 排序字段(title/release_date/total_box_office)
            sort_order: True升序，False降序
        """
        df = self.read_table("movies")  # 读取movies表

        # 按电影名筛选
        if title:
            df = df.filter(F.col("title").contains(title))

        # 按导演筛选
        if director_id:
            movie_directors = self.read_table("movie_directors")
            director_movies = movie_directors.filter(F.col("director_id") == director_id) \
                .select("movie_id").distinct()
            df = df.join(director_movies, "movie_id")

        # 按类型筛选
        if genre_id:
            movie_categories = self.read_table("movie_categories")  # 读取关联表
            movie_ids = movie_categories.filter(F.col("genre_id") == genre_id) \
                .select("movie_id").distinct()  # 获取指定类型的所有电影ID
            df = df.join(movie_ids, "movie_id")  # 内连接获取符合条件的电影

        # 按最低评分筛选
        if min_rating > 0:
            df = df.filter(F.col("overall_rating") >= min_rating)

        # 排序逻辑
        if sort_field in ['title', 'release_date', 'total_box_office']:
            sort_column = F.col(sort_field)
            # 处理release_date的特殊情况(需要转换为日期类型)
            if sort_field == 'release_date':
                sort_column = F.to_date(sort_column)
            # 应用排序方向
            df = df.orderBy(sort_column.asc() if sort_order else sort_column.desc())
        else:
            # 默认按标题升序排序
            df = df.orderBy(F.col("title").asc())
        # 使用窗口函数实现分页
        window = Window.orderBy(F.monotonically_increasing_id())  # 创建一个稳定的排序

        paginated_df = df.withColumn("row_num", F.row_number().over(window)) \
            .filter((F.col("row_num") > (page - 1) * page_size)) \
            .filter(F.col("row_num") <= page * page_size) \
            .drop("row_num")

        return paginated_df.collect()
