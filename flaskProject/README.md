# Requirements 

1. [Java 环境](https://www.oracle.com/java/technologies/downloads)
2. 本地配置 [spark](https://spark.apache.org/downloads.html) lib [(查询对应的 python 和 java 版本)](https://spark.apache.org/docs/latest)
3. python 环境内配置 py4j [(注意 python 版本和 Java 版本对应)](https://www.py4j.org/changelog.html)
4. python 环境内配置 pyspark (要与本地 spark 版本相同)
5. mysql-connector-java
    - [官网](https://dev.mysql.com/downloads/connector/j) 选择 Platform Independent, 下载发行包
    - 将发行包中的 mysql-connector-j-x.x.x.jar 移动到 spark 环境的 jars 目录下
6. python 环境内配置 flask

# TODO

* [ ] json serialization
* [ ] make mapper instance
* [ ] test