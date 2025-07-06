# SCU-MoviesDataAnalysis

## 一、项目说明



## 二、项目启动

### 1.前端启动

1）npm i

2）npm run dev

### 2.数据库连接

1）在Navicat的mysql连接中创建movie_db数据库

2）右键movie_db，选择Execute SQL File，选择/SCU-MoviesDataAnalysis/sql中的movie_db.sql



### 3.后端启动

1）pycharm打开flaskProject，本地环境：spark-3.2.2+python3.8

2）工作目录下在控制台pip install flask

3）把mysql-connector-java包拷贝到spark/jars目录下

4）Pycharm中，Settings->Project Structure->Add Content Root导入spark/python/lib目录下的py4j和pyspark包

5）对于config.py的以下内容：

```
class Config:
    MYSQL_URL = "jdbc:mysql://localhost:3306/movie_db?serverTimezone=Asia/Shanghai"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver"
    SECRET_KEY = "your-secret-key-here"  # 添加这行，使用强密钥
```

把MYSQL_USER和MYSQL_PASSWORD改成本地数据库的用户和密码