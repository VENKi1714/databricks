# Databricks notebook source
dbutils.secrets.list(scope='data_engineering_project')

# COMMAND ----------

def mount_adls(storage_account_name, container_name):
    # Correcting the typo in secret key names
    client_id = dbutils.secrets.get(scope='data_engineering_project', key='secert-client-id')
    tenant_id = dbutils.secrets.get(scope='data_engineering_project', key='secret-tenant-id')
    client_secret = dbutils.secrets.get(scope='data_engineering_project', key='secret-tenant-secret')

    # Set Spark configuration
    configs = {
        "fs.azure.account.auth.type": "OAuth",
        "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        "fs.azure.account.oauth2.client.id": client_id,
        "fs.azure.account.oauth2.client.secret": client_secret,
        "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    }

    # Unmount the mount point if already exists
    if any(mount.mountPoint == f"/mnt/{storage_account_name}/{container_name}" for mount in dbutils.fs.mounts()):
        dbutils.fs.unmount(f"/mnt/{storage_account_name}/{container_name}")

    # Mount the storage account container
    dbutils.fs.mount(
        source=f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
        mount_point=f"/mnt/{storage_account_name}/{container_name}",
        extra_configs=configs
    )

    display(dbutils.fs.mounts())


# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

mount_adls('dataengineringproject','bronze')

# COMMAND ----------

mount_adls('dataengineringproject','sliver')

# COMMAND ----------

mount_adls('dataengineringproject','gold')

# COMMAND ----------

