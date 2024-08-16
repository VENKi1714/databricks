# Databricks notebook source
from pyspark.sql.functions import from_utc_timestamp,date_format
from pyspark.sql.types import TimestampType
import os

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls('/mnt/dataengineringproject/bronze/SalesLT/'):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

for i in table_name:
    path ='/mnt/dataengineringproject/bronze/SalesLT/' + i + '/' + i + '.csv'
    dff = spark.read.csv(path, header=True, inferSchema=True)
    columns = dff.columns

    for col in columns:
        if "Date" in col or "date" in col:
            dff = dff.withColumn(col, date_format(from_utc_timestamp(dff[col].cast(TimestampType()),"UTC"), "yyyy-MM-dd"))

    output_path = '/mnt/dataengineringproject/sliver/SalesLT/' + i + '/'
    dff.write.format('csv').mode('overwrite').save(output_path)
    

# COMMAND ----------

display(dff)