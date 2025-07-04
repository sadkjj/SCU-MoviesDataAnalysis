# mapper/UserMapper.py
from pyspark.sql import functions as F
from pyspark.sql.window import Window  # 导入窗口函数
from mapper.Mapper import Mapper
from datetime import datetime
from config import Config


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
        self.read_table("users").createOrReplaceTempView("users")
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_sql = f"""
            INSERT INTO TABLE users
            SELECT 
                NULL as user_id,
                '{user_data["username"]}' as username,
                '{user_data["password"]}' as password,
                '{user_data.get("real_name", "")}' as real_name,
                '{user_data.get("phone", "")}' as phone,
                {user_data.get("role_type", 2)} as role_type,
                '{user_data.get("email", "")}' as email,
                timestamp('{create_time}') as create_time,
                timestamp('{update_time}') as update_time
        """
        # 执行插入操作
        self.execute_sql(insert_sql)
        # 查询新创建的用户记录
        query_sql = f"""
                SELECT * FROM users 
                WHERE username = '{user_data["username"]}'
                ORDER BY user_id DESC 
                LIMIT 1
            """
        result_df = self.spark.sql(query_sql)

        if result_df.count() > 0:
            user_id = result_df.first().user_id
            return user_id
        return None

    def get_user_by_id(self, user_id):
        """根据ID获取单个用户信息"""
        df = self.read_table("users")
        user = df.filter(F.col("user_id") == user_id).first()
        return user.asDict() if user else None

    def update_user(self, user_id, update_data):
        """使用UPDATE语句更新用户信息"""
        try:
            # JDBC连接配置
            jdbc_url = Config.MYSQL_URL
            connection_properties = {
                "user": Config.MYSQL_USER,
                "password": Config.MYSQL_PASSWORD,
                "driver": Config.MYSQL_DRIVER
            }
            # 创建JDBC连接
            connection = self.spark._jvm.java.sql.DriverManager.getConnection(
                jdbc_url,
                connection_properties["user"],
                connection_properties["password"]
            )
            # 准备UPDATE语句
            update_sql = """
                UPDATE users 
                SET 
                    username = ?,
                    real_name = ?,
                    phone = ?,
                    email = ?,
                    update_time = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """

            # 设置参数
            update_stmt = connection.prepareStatement(update_sql)
            update_stmt.setString(1, update_data['username'])
            update_stmt.setString(2, update_data['real_name'])
            update_stmt.setString(3, update_data['phone'])
            update_stmt.setString(4, update_data['email'])
            update_stmt.setLong(5, user_id)

            # 执行更新
            affected_rows = update_stmt.executeUpdate()
            connection.close()

            return affected_rows > 0

        except Exception as e:
            print(f"更新用户时出错: {str(e)}")
            return False

    def get_movie_list(self, page=1, page_size=10, title=None, genre_id=None, director_id=None, min_rating=0,
                       sort_field='release_date', sort_order=False):
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
        else:
            # 默认按标题升序排序
            sort_column = F.to_date(F.col('release_date'))

        # 添加movie_id作为第二排序条件确保稳定性
        secondary_sort = F.col("movie_id").asc()

        # 应用排序方向
        df = df.orderBy(sort_column.asc() if sort_order else sort_column.desc(), secondary_sort)

        # 使用窗口函数实现分页
        window = Window.orderBy(sort_column.asc() if sort_order else sort_column.desc(), secondary_sort)  # 创建一个稳定的排序

        paginated_df = df.withColumn("row_num", F.row_number().over(window)) \
            .filter((F.col("row_num") > (page - 1) * page_size)) \
            .filter(F.col("row_num") <= page * page_size) \
            .drop("row_num")

        return paginated_df.collect()

    def get_movie_count(self, title=None, genre_id=None, director_id=None, min_rating=0):
        """获取电影总数"""
        df = self.read_table("movies")

        if title:
            df = df.filter(F.col("title").contains(title))
        if genre_id:
            movie_categories = self.read_table("movie_categories")
            movie_ids = movie_categories.filter(F.col("genre_id") == genre_id).select("movie_id").distinct()
            df = df.join(movie_ids, "movie_id")
        if director_id:
            movie_directors = self.read_table("movie_directors")
            director_movies = movie_directors.filter(F.col("director_id") == director_id).select("movie_id").distinct()
            df = df.join(director_movies, "movie_id")
        if min_rating > 0:
            df = df.filter(F.col("overall_rating") >= min_rating)

        return df.count()

    def get_movie_directors(self, movie_id):
        """获取电影导演列表"""
        df = self.read_table("movie_directors").filter(F.col("movie_id") == movie_id)
        directors = self.read_table("directors")
        return df.join(directors, "director_id").select("name").collect()

    def get_movie_actors(self, movie_id):
        """获取电影演员列表"""
        df = self.read_table("movie_actors").filter(F.col("movie_id") == movie_id)
        actors = self.read_table("actors")
        return df.join(actors, "actor_id").select("name").collect()

    def get_movie_genres(self, movie_id):
        """获取电影类型列表"""
        df = self.read_table("movie_categories").filter(F.col("movie_id") == movie_id)
        genres = self.read_table("categories")
        return df.join(genres, "genre_id").select("name").collect()

    def get_movie_director_by_name(self, name):
        """根据导演名获取id"""
        director = self.read_table("directors").filter(F.col("name").contains(name)).first()
        return director["director_id"] if director else None

    def get_movie_genre_by_name(self, name):
        """根据类型名获取id"""
        genre = self.read_table("categories").filter(F.col("name").contains(name)).first()
        return genre["genre_id"] if genre else None
