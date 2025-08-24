from pyspark.sql import SparkSession, DataFrame, Window
from main.base import PySparkJobInterface
import pyspark.sql.functions as F
from typing import Dict


class PySparkJob(PySparkJobInterface):

    def __init__(self):
        self.spark = self.init_spark_session()

    def init_spark_session(self) -> SparkSession:
        return SparkSession.builder.appName('Banking Data Mining').master('local').getOrCreate()

    def read_csv(self, path:str) -> DataFrame:
        return self.spark.read_csv(path,header = True, inferSchema = True)    

    def extract_valid_transactions(self, accounts: DataFrame, transactions: DataFrame) -> DataFrame:
        
        from_accounts = accounts.select(col("accountNumber".alias("fromAccountNumber"), col("balance").alias("fromBalance")))

        valid_from = transactions.join(from_accounts, "fromAccountNumber","inner")

        valid_to_accounts = accounts.select(col("accountNumber").alias("toAccountNumber"))

        valid_transactions = valid_from.join(valid_to_accounts, "toAccountNumber","inner").filter(col("transferAmount") <= col("fromBalance"))

        return valid_transactions.select("fromAccountNumber","toAccountNumber","transferAmount")


    def distinct_transactions(self, transactions: DataFrame) -> int:
        return transactions.select("fromAccountNumber").distinct().count()

    def transactions_per_account(self, transactions: DataFrame) -> DataFrame:
        result_df = transactions.groupBy("fromAccountNumber").agg(count("*").alias("transactionCount")).orderBy(desc("transactionCount")).limit(10)

        return {row["fromAccountNumber"]: row["transactionCount"] for row in result_df.collect()}
