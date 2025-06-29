import os
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"
os.environ["PYSPARK_PYTHON"] = "python"
from pyspark.sql import SparkSession
if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordcount").master("local[2]").getOrCreate()
    sc = spark.sparkContext
    fileRDD = sc.textFile(r"D:\Workspace\LLM_JK\data\wordcount.data")
    wordRDD = fileRDD.flatMap(lambda line: line.split(" "))
    word2OneRDD=wordRDD.map(lambda word:(word,1))
    word2CountRDD=word2OneRDD.reduceByKey(lambda a,b:a+b)
    result =word2CountRDD.collect()
    print(result)
