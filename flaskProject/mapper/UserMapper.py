from pyspark.sql import SparkSession
from config import Config


class UserMapper:
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()
        self.url = Config.MYSQL_URL
        self.user = Config.MYSQL_USER
        self.password = Config.MYSQL_PASSWORD
        self.driver = Config.MYSQL_DRIVER

    def get_user_by_id(self, user_id):
        query = f"(SELECT * FROM users WHERE user_id = '{user_id}') as user_query"
        df = self.spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .load()

        if df.count() > 0:
            return df.first().asDict()
        return None

    def create_user(self, user_id, password):
        # 注意：实际应用中密码应该加密存储
        new_user = self.spark.createDataFrame([(user_id, password)], ["user_id", "password"])
        new_user.write.format("jdbc") \
            .option("url", self.url) \
            .option("driver", self.driver) \
            .option("dbtable", "users") \
            .option("user", self.user) \
            .option("password", self.password) \
            .mode("append") \
            .save()

        return True