# Task scheduler #

> Rewrite the class "BackgroundTaskScheduler" from Swift to C++, BackgroundTaskScheduler maintain a 
> background thread, and periedly check all registered tasks if they need running, the duration should > be config in a constant, and run  task that responed "true" for "shouldTriggerSinceLast" on the 
> background thread when trigger, record the last running time and call "shouldTriggerSinceLast" for
> next time.

### Sample interface

```Swift
import Foundation

class Task {
    func runOnce() {}
    func shouldTriggerSinceLast(_ duration: TimeInterval) -> Bool {
        return true
    }
}

class BackgroundTaskScheduler {
    static let sharedInstance: BackgroundTaskScheduler = BackgroundTaskScheduler()
    func registerTask(_ task: Task, name: String) { }
    func removeTaskNamed(_ name: String) {}
    func removeAllTask() {}
    func start() {}
    func stop() {}
    func onTrigger() {}
}
```
### Sample interface

Here’s the implementation with separate header files for each class. Additionally, a sample `SampleTask` subclass demonstrates task functionality.

### `Task.h`

```cpp
#ifndef TASK_H
#define TASK_H

#include <chrono>

class Task {
public:
    virtual ~Task() = default;
    virtual void runOnce();  // Define task execution behavior
    virtual bool shouldTriggerSinceLast(std::chrono::seconds duration);  // Check if task should trigger
};

#endif  // TASK_H
```

### `Task.cpp`

```cpp
#include "Task.h"
#include <iostream>

void Task::runOnce() {
    // Define task execution behavior (placeholder)
    std::cout << "Running Task" << std::endl;
}

bool Task::shouldTriggerSinceLast(std::chrono::seconds duration) {
    // Check condition to trigger task (placeholder)
    return true;
}
```

### `BackgroundTaskScheduler.h`

```cpp
#ifndef BACKGROUNDTASKSCHEDULER_H
#define BACKGROUNDTASKSCHEDULER_H

#include "Task.h"
#include <string>
#include <unordered_map>
#include <thread>
#include <chrono>
#include <atomic>
#include <mutex>
#include <memory>

class BackgroundTaskScheduler {
public:
    static BackgroundTaskScheduler& sharedInstance();

    void registerTask(std::shared_ptr<Task> task, const std::string& name);
    void removeTaskNamed(const std::string& name);
    void removeAllTasks();
    void start();
    void stop();

private:
    BackgroundTaskScheduler();
    ~BackgroundTaskScheduler();

    void onTrigger();

    struct TaskInfo {
        std::shared_ptr<Task> task;
        std::chrono::time_point<std::chrono::steady_clock> lastRun;
    };

    std::unordered_map<std::string, TaskInfo> tasks;
    std::thread schedulerThread;
    std::mutex tasksMutex;
    std::atomic<bool> stopFlag{false};
};

#endif  // BACKGROUNDTASKSCHEDULER_H
```

### `BackgroundTaskScheduler.cpp`

```cpp
#include "BackgroundTaskScheduler.h"
#include <iostream>

constexpr std::chrono::seconds CHECK_INTERVAL = std::chrono::seconds(30);

BackgroundTaskScheduler& BackgroundTaskScheduler::sharedInstance() {
    static BackgroundTaskScheduler instance;
    return instance;
}

BackgroundTaskScheduler::BackgroundTaskScheduler() = default;

BackgroundTaskScheduler::~BackgroundTaskScheduler() {
    stop();
}

void BackgroundTaskScheduler::registerTask(std::shared_ptr<Task> task, const std::string& name) {
    std::lock_guard<std::mutex> lock(tasksMutex);
    tasks[name] = {task, std::chrono::steady_clock::now()};
}

void BackgroundTaskScheduler::removeTaskNamed(const std::string& name) {
    std::lock_guard<std::mutex> lock(tasksMutex);
    tasks.erase(name);
}

void BackgroundTaskScheduler::removeAllTasks() {
    std::lock_guard<std::mutex> lock(tasksMutex);
    tasks.clear();
}

void BackgroundTaskScheduler::start() {
    stopFlag = false;
    schedulerThread = std::thread(&BackgroundTaskScheduler::onTrigger, this);
}

void BackgroundTaskScheduler::stop() {
    stopFlag = true;
    if (schedulerThread.joinable()) {
        schedulerThread.join();
    }
}

void BackgroundTaskScheduler::onTrigger() {
    while (!stopFlag) {
        std::this_thread::sleep_for(CHECK_INTERVAL);

        std::lock_guard<std::mutex> lock(tasksMutex);
        auto now = std::chrono::steady_clock::now();

        for (auto& [name, taskInfo] : tasks) {
            auto& [task, lastRun] = taskInfo;
            auto durationSinceLastRun = std::chrono::duration_cast<std::chrono::seconds>(now - lastRun);

            if (task->shouldTriggerSinceLast(durationSinceLastRun)) {
                task->runOnce();
                taskInfo.lastRun = std::chrono::steady_clock::now();
            }
        }
    }
}
```

### `SampleTask.h`

```cpp
#ifndef SAMPLETASK_H
#define SAMPLETASK_H

#include "Task.h"

class SampleTask : public Task {
public:
    void runOnce() override;
    bool shouldTriggerSinceLast(std::chrono::seconds duration) override;
};

#endif  // SAMPLETASK_H
```

### `SampleTask.cpp`

```cpp
#include "SampleTask.h"
#include <iostream>

void SampleTask::runOnce() {
    std::cout << "SampleTask is running!" << std::endl;
}

bool SampleTask::shouldTriggerSinceLast(std::chrono::seconds duration) {
    // Example condition: trigger if more than 10 seconds since last run
    return duration > std::chrono::seconds(10);
}
```

### Example Usage

Here’s a main function demonstrating how to use the scheduler with `SampleTask`:

```cpp
#include "BackgroundTaskScheduler.h"
#include "SampleTask.h"

int main() {
    auto task = std::make_shared<SampleTask>();
    BackgroundTaskScheduler::sharedInstance().registerTask(task, "sample_task");

    BackgroundTaskScheduler::sharedInstance().start();

    // Let the scheduler run for a while
    std::this_thread::sleep_for(std::chrono::seconds(60));

    BackgroundTaskScheduler::sharedInstance().stop();
    return 0;
}
```

### Explanation:

1. `SampleTask` is a subclass of `Task` with custom `runOnce` and `shouldTriggerSinceLast` methods.
2. In `main`, `SampleTask` is registered and executed based on `shouldTriggerSinceLast`.