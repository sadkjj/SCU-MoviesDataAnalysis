# mapper/AdminMapper.py
from datetime import datetime
from mapper.Mapper import Mapper
from pyspark.sql import functions as F
from pyspark.sql.window import Window  # 导入窗口函数
from config import Config


class AdminMapper(Mapper):
    def __init__(self):
        super().__init__()

    def get_user_count(self, search=None):
        """获取用户总数"""
        df = self.read_table("users")
        if search:
            df = df.filter(F.col("username").contains(search))
        return df.count()

    def get_user_by_username(self, username):
        """根据用户名获取用户信息"""
        df = self.read_table("users")
        user = df.filter(F.col("username") == username).first()
        return user.asDict() if user else None  # 将Row对象转为字典或返回None

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
        valid_sort_fields = ['username', 'create_time']
        if sort_field in valid_sort_fields:
            sort_column = F.col(sort_field)
        else:
            sort_column = F.to_timestamp('create_time')

        # 添加user_id作为第二排序条件确保稳定性
        secondary_sort = F.col("user_id").asc()

        # 排序方向
        df = df.orderBy(sort_column.asc() if sort_order else sort_column.desc(), secondary_sort)

        # 使用与主排序相同的字段定义窗口
        window_spec = Window.orderBy(sort_column.asc() if sort_order else sort_column.desc(), secondary_sort)

        paginated_df = df.withColumn("row_num", F.row_number().over(window_spec)) \
            .filter((F.col("row_num") > (page - 1) * page_size)) \
            .filter(F.col("row_num") <= page * page_size) \
            .drop("row_num")

        return paginated_df.collect()

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
                '{user_data["real_name"]}' as real_name,
                '{user_data["phone"]}' as phone,
                {user_data.get("role_type", 2)} as role_type,
                '{user_data["email"]}' as email,
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
                    role_type = ?,
                    update_time = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """

            # 设置参数
            update_stmt = connection.prepareStatement(update_sql)
            update_stmt.setString(1, update_data['username'])
            update_stmt.setString(2, update_data['real_name'])
            update_stmt.setString(3, update_data['phone'])
            update_stmt.setString(4, update_data['email'])
            update_stmt.setInt(5, update_data['role_type'])
            update_stmt.setLong(6, user_id)
            # 执行更新
            affected_rows = update_stmt.executeUpdate()
            connection.close()

            return affected_rows > 0

        except Exception as e:
            print(f"更新用户时出错: {str(e)}")
            return False

    def delete_user(self, user_id):
        """使用JDBC直接连接MySQL执行删除"""
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

            # 准备DELETE语句
            delete_stmt = connection.prepareStatement(f"""
                DELETE FROM users WHERE user_id = {user_id}
            """)

            # 执行并返回影响的行数
            affected_rows = delete_stmt.executeUpdate()
            connection.close()

            return affected_rows > 0
        except Exception as e:
            print(f"删除用户时出错: {str(e)}")
            return False


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
        try:
            self.spark.sql("START TRANSACTION")
            for table in ["movie_directors", "movie_actors", "movie_categories"]:
                df = self.read_table(table)  # 读取关联表
                df = df.filter(F.col("movie_id") != movie_id)
                self.write_table(df, table, mode="overwrite")
            # 删除电影主表
            df = self.read_table("movies")
            df = df.filter(F.col("movie_id") != movie_id)
            self.write_table(df, "movies", mode="overwrite")
            self.spark.sql("COMMIT")
            return True
        except:
            self.spark.sql("ROLLBACK")
            raise
