# mapper/AdminMapper.py
from pyspark.sql import functions as F
from pyspark.sql.window import Window  # 导入窗口函数
from mapper.Mapper import Mapper


class AdminMapper(Mapper):
    def __init__(self):
        super().__init__()

    def get_user_list(self, page=1, page_size=10, sort_field='create_time', sort_order=False, search=None):
        """获取用户列表
        参数:
        page: 页码(从1开始)
        page_size: 每页大小（默认10）
        sort_field: 排序字段(username/create_time)
        sort_order: True升序，False降序
        search: 搜索关键词（模糊匹配用户名）
        """
        df = self.read_table("users")

        # 根据搜索内容筛选
        if search:
            search = search.strip()  # 去除前后空格
            if search:
                search_condition = (F.col("username").contains(search))
                df = df.filter(search_condition)

        # 排序处理
        valid_sort_fields = ['username', 'real_name', 'phone', 'email', 'create_time']
        if sort_field in valid_sort_fields:
            sort_column = F.col(sort_field)
            # 对时间字段特殊处理
            if sort_field == 'create_time':
                sort_column = F.to_timestamp(sort_column)
            # 排序方向
            df = df.orderBy(sort_column.asc() if sort_order else sort_column.desc())
        else:
            # 默认按创建时间降序
            df = df.orderBy(F.col("create_time").desc())

        # 使用与主排序相同的字段定义窗口
        window_spec = Window.orderBy(F.col(sort_field if sort_field in valid_sort_fields else "create_time"))
        paginated_df = df.withColumn("row_num", F.row_number().over(window_spec)) \
            .filter((F.col("row_num") > (page - 1) * page_size)) \
            .filter(F.col("row_num") <= page * page_size) \
            .drop("row_num")

        return paginated_df.collect()

    def create_user(self, user_data):
        """创建用户"""
        from pyspark.sql import Row
        new_user = Row(**user_data)
        df = self.spark.createDataFrame([new_user])
        self.write_table(df, "users")
        return True

    def update_user(self, user_id, update_data):
        """管理员更新用户信息"""
        df = self.read_table("users")
        for key, value in update_data.items():
            df = df.withColumn(key,
                               F.when(F.col("user_id") == user_id, value).otherwise(F.col(key)))
        self.write_table(df, "users", mode="overwrite")
        return True

    def delete_user(self, user_id):
        """删除用户"""
        df = self.read_table("users")
        df = df.filter(F.col("user_id") != user_id)
        self.write_table(df, "users", mode="overwrite")
        return True

    # def create_movie(self, movie_data):
    #     """创建电影"""
    #     from pyspark.sql import Row
    #     new_movie = Row(**movie_data)
    #     df = self.spark.createDataFrame([new_movie])
    #     self.write_table(df, "movies")
    #     return True
    #
    # def update_movie(self, movie_id, update_data):
    #     """更新电影信息"""
    #     df = self.read_table("movies")
    #     for key, value in update_data.items():
    #         df = df.withColumn(key,
    #                            F.when(F.col("movie_id") == movie_id, value).otherwise(F.col(key)))
    #     self.write_table(df, "movies", mode="overwrite")
    #     return True

    def delete_movie(self, movie_id):
        """删除电影"""
        # 删除关联表数据
        for table in ["movie_directors", "movie_actors", "movie_categories"]:
            df = self.read_table(table)  # 读取关联表
            df = df.filter(F.col("movie_id") != movie_id)
            self.write_table(df, table, mode="overwrite")

        # 删除电影主表
        df = self.read_table("movies")
        df = df.filter(F.col("movie_id") != movie_id)
        self.write_table(df, "movies", mode="overwrite")
        return True
