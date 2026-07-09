from clickhouse_driver import Client
from app.core.config import settings

client = Client(host=settings.CLICKHOUSE_URL.replace("http://", "").replace(":8123", ""))

def init_clickhouse():
    client.execute(f"CREATE DATABASE IF NOT EXISTS {settings.CLICKHOUSE_DATABASE}")
    
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.CLICKHOUSE_DATABASE}.metrics (
            device_id Int32,
            metric_type String,
            value Float64,
            timestamp DateTime
        ) ENGINE = MergeTree()
        ORDER BY (device_id, timestamp)
    """)
    
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.CLICKHOUSE_DATABASE}.logs (
            device_id Int32,
            log_type String,
            level String,
            message String,
            timestamp DateTime
        ) ENGINE = MergeTree()
        ORDER BY (device_id, timestamp)
    """)
    
    print("ClickHouse tables created successfully")

if __name__ == "__main__":
    init_clickhouse()