from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import app, db
import pymysql
pymysql.install_as_MySQLdb()

# 创建flask脚本管理工具对象
manager = Manager(app)

# 创建数据库迁移工具对象
Migrate(app, db)

# 向manager对象中添加数据库的操作命令
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()