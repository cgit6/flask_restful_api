## SQL Alchemy 中的一對多關係

### SQLite

SQLite 預設不會強制執行 foreign key 約束，這意味著即使您在資料庫表中定義了外部約束，SQLite 也不會自動檢查這些外部約束，如果不滿足，這可能會導致資料引用完整性問題。

### 为什么 SQLite 默认不启用 foreign key 约束

SQLite 是一个轻量级的数据库系统，设计时侧重于简便性和灵活性。为了最大限度地提高性能和减少资源使用，很多数据库功能（包括 foreign key 约束的强制执行）在默认设置中是禁用的。这样可以让 SQLite 运行在资源有限的环境中，如嵌入式设备或移动应用，而不会因为处理复杂的约束检查而导致性能问题。

### 如何启用 foreign key 约束

如果你需要在 SQLite 数据库中启用 foreign key 约束，必须在每次连接到数据库时显式地启用它们。这可以通过执行 SQL 命令 `PRAGMA foreign_keys = ON;` 来完成。这个命令告诉 SQLite 在当前的数据库连接中启用 foreign key 约束检查。

例如，在 Python 中使用 SQLite 时，可以如下操作：

```python
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('example.db')

# 创建一个 Cursor 对象并启用foreign key 约束
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# 之后就可以执行其他数据库操作，foreign key 约束将被强制执行
# 例如，创建表、插入数据等
```

### 启用 foreign key 约束的影响

启用 foreign key 约束后，SQLite 将检查所有的 INSERT 和 UPDATE 操作，确保所有的 foreign key 約束都引用了主键表中存在的记录。如果尝试插入或更新一个违反 foreign key 約束的记录，操作将失败，并返回一个错误。这有助于维护数据库的数据完整性和一致性。

## SQL Alchemy 中的多對多關係

線上商店使用標籤(tag)對 item 進行分組
