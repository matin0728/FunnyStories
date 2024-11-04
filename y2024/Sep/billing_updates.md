# Updated billing module implementation #

# Refactor "BillingDBHelper::findRecords" to return instances of "BillableEvent", and update files related. #

Here’s the refactored code where `BillingDBHelper::findRecords` returns instances of a new class, `BillableEvent`, and all necessary updates have been applied to related files.

### **1. `BillableEvent.h` (New Class)**
```cpp
#ifndef BILLABLEEVENT_H
#define BILLABLEEVENT_H

#include <string>

class BillableEvent {
public:
    std::string id;
    std::string time;
    int quantify;

    BillableEvent(const std::string& id, const std::string& time, int quantify);
};

#endif // BILLABLEEVENT_H
```

### **2. `BillableEvent.cpp`**
```cpp
#include "BillableEvent.h"

BillableEvent::BillableEvent(const std::string& id, const std::string& time, int quantify)
    : id(id), time(time), quantify(quantify) {}
```

---

### **3. `BillingDBHelper.h` (Updated)**
```cpp
#ifndef BILLINGDBHELPER_H
#define BILLINGDBHELPER_H

#include <vector>
#include <string>
#include <sqlite3.h>
#include <mutex>
#include "BillableEvent.h"

class BillingDBHelper {
private:
    std::string dbPath;
    std::mutex dbMutex;

    bool openDatabase(sqlite3** db);
    void closeDatabase(sqlite3* db);

public:
    BillingDBHelper(const std::string& path);

    std::vector<BillableEvent> findRecords(int limit);
    void deleteRecords(const std::vector<std::string>& ids);
};

#endif // BILLINGDBHELPER_H
```

---

### **4. `BillingDBHelper.cpp` (Updated)**
```cpp
#include "BillingDBHelper.h"
#include <iostream>

BillingDBHelper::BillingDBHelper(const std::string& path) : dbPath(path) {}

bool BillingDBHelper::openDatabase(sqlite3** db) {
    if (sqlite3_open(dbPath.c_str(), db) != SQLITE_OK) {
        std::cerr << "Can't open database: " << sqlite3_errmsg(*db) << std::endl;
        return false;
    }
    return true;
}

void BillingDBHelper::closeDatabase(sqlite3* db) {
    if (db) {
        sqlite3_close(db);
    }
}

std::vector<BillableEvent> BillingDBHelper::findRecords(int limit) {
    std::lock_guard<std::mutex> lock(dbMutex);
    std::vector<BillableEvent> events;
    sqlite3* db = nullptr;

    if (!openDatabase(&db)) {
        return events;
    }

    std::string query = "SELECT id, time, quantify FROM events LIMIT " + std::to_string(limit) + ";";
    sqlite3_stmt* stmt;
    if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        closeDatabase(db);
        return events;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::string id = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        std::string time = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        int quantify = sqlite3_column_int(stmt, 2);

        events.emplace_back(id, time, quantify);  // Create BillableEvent and add to list
    }
    sqlite3_finalize(stmt);
    closeDatabase(db);
    return events;
}

void BillingDBHelper::deleteRecords(const std::vector<std::string>& ids) {
    std::lock_guard<std::mutex> lock(dbMutex);
    sqlite3* db = nullptr;

    if (!openDatabase(&db)) {
        return;
    }

    for (const std::string& id : ids) {
        std::string query = "DELETE FROM events WHERE id = '" + id + "';";
        char* errMsg;
        if (sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
    }
    closeDatabase(db);
}
```

---

### **5. `BillingManager.h` (Updated)**
```cpp
#ifndef BILLINGMANAGER_H
#define BILLINGMANAGER_H

#include <string>
#include <functional>
#include <vector>
#include "BillableEvent.h"

class BillingManager {
private:
    std::string endpoint;
    std::string credentials;

public:
    BillingManager(const std::string& endpoint, const std::string& credentials);

    void uploadEvents(const std::vector<BillableEvent>& events, std::function<void(bool)> callback);
};

#endif // BILLINGMANAGER_H
```

---

### **6. `BillingManager.cpp` (Updated)**
```cpp
#include "BillingManager.h"
#include <curl/curl.h>
#include <iostream>
#include <json/json.h>

BillingManager::BillingManager(const std::string& endpoint, const std::string& credentials)
    : endpoint(endpoint), credentials(credentials) {}

void BillingManager::uploadEvents(const std::vector<BillableEvent>& events, std::function<void(bool)> callback) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Failed to initialize CURL" << std::endl;
        callback(false);
        return;
    }

    // Convert BillableEvent to JSON string
    Json::Value jsonEvents(Json::arrayValue);
    for (const auto& event : events) {
        Json::Value jsonEvent;
        jsonEvent["id"] = event.id;
        jsonEvent["time"] = event.time;
        jsonEvent["quantify"] = event.quantify;
        jsonEvents.append(jsonEvent);
    }
    Json::StreamWriterBuilder writer;
    std::string jsonData = Json::writeString(writer, jsonEvents);

    curl_easy_setopt(curl, CURLOPT_URL, endpoint.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());

    // Set HTTP headers
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    CURLcode res = curl_easy_perform(curl);

    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        callback(false);
    } else {
        callback(true);
    }

    // Cleanup
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
}
```

---

### **7. `MetricsUploadManager.cpp` (Updated to Use `BillableEvent`)**
```cpp
#include "MetricsUploadManager.h"
#include <iostream>

MetricsUploadManager::MetricsUploadManager(BillingManager* bm, BillingDBHelper* dbh)
    : billingManager(bm), dbHelper(dbh) {}

void MetricsUploadManager::run(bool immediate) {
    std::unique_lock<std::mutex> lock(mtx);
    if (!immediate) {
        cv.wait_for(lock, std::chrono::seconds(30));
    }
    while (!stopFlag) {
        onTrigger();
        cv.wait_for(lock, std::chrono::seconds(30));
    }
}

void MetricsUploadManager::start(bool immediate) {
    internalThread = std::thread(&MetricsUploadManager::run, this, immediate);
}

void MetricsUploadManager::onTrigger() {
    // Fetch records synchronously on the working thread
    std::vector<BillableEvent> events = dbHelper->findRecords(10);
    
    if (!events.empty()) {
        // Upload events synchronously on the working thread
        billingManager->uploadEvents(events, [this, events](bool success) {
            if (success) {
                std::vector<std::string> ids;
                for (const auto& event : events) {
                    ids.push_back(event.id);
                }
                dbHelper->deleteRecords(ids);  // Synchronous deletion after successful upload
            } else {
                std::cerr << "Upload failed. Retrying next time." << std::endl;
            }
        });
    }
}

void MetricsUploadManager::stop() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        stopFlag = true;
    }
    cv.notify_all();
    if (internalThread.joinable()) {
        internalThread.join();
    }
}
```

---

### Summary of Changes:
1. **New Class `BillableEvent`**: Introduced to represent the structure of events fetched from the database.
2. **`BillingDBHelper::findRecords`**: Now returns a list of `BillableEvent` instances instead of `Json::Value`.
3. **`BillingManager::uploadEvents`**: Modified to accept a vector of `BillableEvent` objects and convert them to JSON before uploading.
4. **Thread-Safe Execution**: All operations continue to be performed synchronously on the internal thread, using the refactored `BillableEvent`.

This version keeps all database access and network operations safe, efficient, and consistent with the requested changes.