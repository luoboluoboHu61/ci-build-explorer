import sqlite3

DB_NAME = "data/builds.db"

# 初始化数据库（建表）
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS builds (
            id INTEGER PRIMARY KEY,
            status TEXT,
            conclusion TEXT,
            branch TEXT,
            commit_msg TEXT,
            start_time TEXT,
            end_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 插入构建记录
def insert_builds(builds):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for build in builds:
        cursor.execute('''
            INSERT OR REPLACE INTO builds (id, status, conclusion, branch, commit_msg, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            build['id'],
            build['status'],
            build['conclusion'],
            build['branch'],
            build['commit_msg'],
            build['start_time'],
            build['end_time']
        ))
    conn.commit()
    conn.close()

# 查询所有记录
def fetch_all_builds():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM builds ORDER BY start_time DESC")
    rows = cursor.fetchall()
    conn.close()

    keys = ['id', 'status', 'conclusion', 'branch', 'commit_msg', 'start_time', 'end_time']
    return [dict(zip(keys, row)) for row in rows]
