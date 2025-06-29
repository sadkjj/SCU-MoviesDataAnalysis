class Config:
    MYSQL_URL = "jdbc:mysql://localhost:3306/movie_db?serverTimezone=Asia/Shanghai"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver"
    SECRET_KEY = "your-secret-key-here"  # 添加这行，使用强密钥
