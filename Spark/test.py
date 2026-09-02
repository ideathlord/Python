import findspark
findspark.init() # This is often helpful to locate Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MySparkApp") \
    .getOrCreate()

print("SparkSession created successfully!")
spark.stop()