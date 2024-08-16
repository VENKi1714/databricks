# Databricks notebook source
table_name = []

for i in dbutils.fs.ls('/mnt/dataengineringproject/sliver/SalesLT/'):
    table_name.append(i.name.split('/')[0])