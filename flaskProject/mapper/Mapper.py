# mapper/BasicMapper.py
from pyspark.sql import SparkSession
from config import Config


class Mapper:
    def __init__(self):
        self.spark = SparkSession.builder.appName("MovieDB").getOrCreate()
        self.mysql_url = Config.MYSQL_URL
        self.mysql_props = {
            "user": Config.MYSQL_USER,
            "password": Config.MYSQL_PASSWORD,
            "driver": Config.MYSQL_DRIVER
        }

    def read_table(self, table_name):
        """读取整张表"""
        return self.spark.read.jdbc(
            url=self.mysql_url,
            table=table_name,
            properties=self.mysql_props
        )

    def write_table(self, df, table_name, mode="append"):
        """写入数据到表"""
        df.write.jdbc(
            url=self.mysql_url,
            table=table_name,
            mode=mode,
            properties=self.mysql_props
        )

    def execute_sql(self, sql):
        """执行SQL语句"""
        return self.spark.sql(sql)

    def close(self):
        """关闭Spark会话"""
        self.spark.stop()