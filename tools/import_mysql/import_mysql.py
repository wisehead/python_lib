import mysql.connector
import pandas as pd
from typing import List, Dict
import logging

class MySQLImporter:
    def __init__(self, host: str, user: str, password: str, database: str):
        """初始化MySQL连接参数"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """建立MySQL连接"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            logging.info("数据库连接成功")
        except Exception as e:
            logging.error(f"数据库连接失败: {str(e)}")
            raise

    def import_from_csv(self, file_path: str, table_name: str):
        """从CSV文件导入数据到MySQL表"""
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 生成插入SQL
            columns = ','.join(df.columns)
            values = ','.join(['%s'] * len(df.columns))
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            # 执行批量插入
            data = [tuple(row) for row in df.values]
            self.cursor.executemany(insert_sql, data)
            self.conn.commit()
            
            logging.info(f"成功导入 {len(data)} 条数据到表 {table_name}")
            
        except Exception as e:
            self.conn.rollback()
            logging.error(f"数据导入失败: {str(e)}")
            raise
            
    def import_from_dict(self, data: List[Dict], table_name: str):
        """从字典列表导入数据到MySQL表"""
        try:
            if not data:
                logging.warning("没有数据需要导入")
                return
                
            # 生成插入SQL
            columns = ','.join(data[0].keys())
            values = ','.join(['%s'] * len(data[0]))
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            # 执行批量插入
            values_list = [tuple(d.values()) for d in data]
            self.cursor.executemany(insert_sql, values_list)
            self.conn.commit()
            
            logging.info(f"成功导入 {len(data)} 条数据到表 {table_name}")
            
        except Exception as e:
            self.conn.rollback()
            logging.error(f"数据导入失败: {str(e)}")
            raise
            
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logging.info("数据库连接已关闭")

# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 初始化导入器
    importer = MySQLImporter(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )
    
    try:
        # 连接数据库
        importer.connect()
        
        # 从CSV导入数据
        importer.import_from_csv("data.csv", "test_table")
        
        # 从字典列表导入数据
        test_data = [
            {"name": "张三", "age": 25},
            {"name": "李四", "age": 30}
        ]
        importer.import_from_dict(test_data, "test_table")
        
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")
    finally:
        importer.close()
