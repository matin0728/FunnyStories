# Sqlite database is locked when multiple threads access #

> When I access a Sqlite database from ReactNative and another background thread read and write > it at the same time in a iOS app, it reports a "database file is locked" error, how can I 
> address that?

The "database file is locked" error occurs when two or more threads attempt to access the SQLite database simultaneously, and SQLite's default locking mechanism prevents this. To address this issue, you can consider the following approaches:

### 1. **Use Serialized Mode for Database Access**
SQLite can be configured to handle concurrent reads and writes safely by enabling serialized mode. This ensures that all database operations are executed serially, preventing concurrent access issues.

To enable serialized mode, ensure the database connection is created with the `SQLITE_OPEN_FULLMUTEX` flag:

```cpp
sqlite3_open_v2("your_database_path.db", &db, SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_FULLMUTEX, nullptr);
```

### 2. **Use a Single Shared Database Connection**
Instead of creating multiple database connections, try using a single shared connection across all threads. This approach simplifies handling locks and reduces the chance of encountering the "database file is locked" error. Ensure that all your reads and writes use the same connection.

### 3. **Queue Database Operations Using a Serial Dispatch Queue**
For an iOS app, you can manage database operations using a serial `DispatchQueue`. By queuing all reads and writes on this serial queue, you can ensure only one operation occurs at a time, avoiding concurrency issues.

Here’s how you can implement it:

```swift
let databaseQueue = DispatchQueue(label: "com.yourapp.database")

func readFromDatabase() {
    databaseQueue.async {
        // Perform read operation here
    }
}

func writeToDatabase() {
    databaseQueue.async {
        // Perform write operation here
    }
}
```

### 4. **Enable WAL (Write-Ahead Logging) Mode**
Write-Ahead Logging (WAL) mode allows for concurrent reads and writes by separating the write operations into a different log file. This can help reduce the chance of the "database file is locked" error.

To enable WAL mode, execute the following SQL command right after opening the database:

```sql
PRAGMA journal_mode=WAL;
```

In your code:

```swift
sqlite3_exec(db, "PRAGMA journal_mode=WAL;", nullptr, nullptr, nullptr);
```

### 5. **Retry on Lock**
Implement a retry mechanism when encountering a locked database error. This can be useful if your operations are short and the database will be unlocked quickly:

```swift
var result: Int32
repeat {
    result = sqlite3_step(statement)
    if result == SQLITE_BUSY {
        usleep(10000) // Wait for 10ms
    }
} while result == SQLITE_BUSY
```

### 6. **Database Connection Pooling**
You can implement a connection pool where a limited number of connections are created and reused. Each connection is responsible for handling its own read and write transactions, and the pooling logic ensures that concurrent access is properly managed.

Combining one or more of these approaches should help you address the database locking issues in your React Native app on iOS.