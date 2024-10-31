# Task scheduler 2 #

```
Rewrite following Swift code to C++, create separated header file for each class.

class Task {
    init() {
        
    }

    func runOnce() {}
    func shouldTriggerSinceLast(_ duration: TimeInterval) -> Bool {
        return true
    }
}

class BackgroundTaskScheduler {
    func registerTask(_ task: Task, name: String) { }
    func removeTaskNamed(_ name: String) {}
    func removeAllTask() {}
    func start() {}
    func stop() {}
    func onTrigger() {}
}

class TaskA: Task {
    var token: String
    
    init(token: String) {
        super.init()
        self.token = token
    }
    
    func updateToken(_ theToken: String) {
        self.token = theToken
    }
    
    override func runOnce() {
        print("class A run once.")
    }
    
    override func shouldTriggerSinceLast(_ duration: TimeInterval) -> Bool {
        return duration >= 30
    }
}

class BDependency {
    
}

class TaskB: Task {
    let dbPath: Path
    let depen: BDependency
    
    init(dbPath: Path, depen: BDependency) {
        self.dbPath = dbPath
        self.depen = depen
        super.init()
    }
    
    override func runOnce() {
        print("class B run once.")
    }
    
    override func shouldTriggerSinceLast(_ duration: TimeInterval) -> Bool {
        return duration >= 30
    }
}

static let taskAName: String = "taskA"

class MyScheduler: BackgroundTaskScheduler {
    var taskA: TaskA?
    let taskB: TaskB
        
    static let shared = MyScheduler()
    
    init() {
        self.taskB = TaskB(dbPath: "", depen: BDependency())
        super.init()
        
        self.registerTask(self.taskB, name: "B")
    }
    
    func setupToken(_ token: String) {
        guard taskA == nil else { return }
        let aTask = TaskA(token: token)
        self.taskA = aTask
        self.registerTask(aTask, name: "A")
    }
}

func main() {
    MyScheduler.shared.start()
    MyScheduler.shared.taskA?.updateToken("new token")
}
```

Here's the translated C++ code with each class in its own header and implementation file. Each file follows a typical structure with necessary includes and uses C++ idioms to replicate the Swift class behavior.

### Task.h
```cpp
#ifndef TASK_H
#define TASK_H

#include <chrono>

class Task {
public:
    Task() = default;
    virtual ~Task() = default;

    virtual void runOnce();
    virtual bool shouldTriggerSinceLast(double duration) const;
};

#endif // TASK_H
```

### Task.cpp
```cpp
#include "Task.h"
#include <iostream>

void Task::runOnce() {}

bool Task::shouldTriggerSinceLast(double duration) const {
    return true;
}
```

### BackgroundTaskScheduler.h
```cpp
#ifndef BACKGROUNDTASKSCHEDULER_H
#define BACKGROUNDTASKSCHEDULER_H

#include <string>
#include "Task.h"

class BackgroundTaskScheduler {
public:
    virtual ~BackgroundTaskScheduler() = default;

    void registerTask(Task* task, const std::string& name);
    void removeTaskNamed(const std::string& name);
    void removeAllTasks();
    void start();
    void stop();
    void onTrigger();
};

#endif // BACKGROUNDTASKSCHEDULER_H
```

### BackgroundTaskScheduler.cpp
```cpp
#include "BackgroundTaskScheduler.h"
#include <iostream>
#include <map>

void BackgroundTaskScheduler::registerTask(Task* task, const std::string& name) {
    // Register the task
}

void BackgroundTaskScheduler::removeTaskNamed(const std::string& name) {
    // Remove specific task
}

void BackgroundTaskScheduler::removeAllTasks() {
    // Remove all tasks
}

void BackgroundTaskScheduler::start() {
    // Start scheduler
}

void BackgroundTaskScheduler::stop() {
    // Stop scheduler
}

void BackgroundTaskScheduler::onTrigger() {
    // Trigger action
}
```

### TaskA.h
```cpp
#ifndef TASKA_H
#define TASKA_H

#include "Task.h"
#include <string>

class TaskA : public Task {
private:
    std::string token;

public:
    explicit TaskA(const std::string& token);
    void updateToken(const std::string& newToken);
    void runOnce() override;
    bool shouldTriggerSinceLast(double duration) const override;
};

#endif // TASKA_H
```

### TaskA.cpp
```cpp
#include "TaskA.h"
#include <iostream>

TaskA::TaskA(const std::string& token) : token(token) {}

void TaskA::updateToken(const std::string& newToken) {
    token = newToken;
}

void TaskA::runOnce() {
    std::cout << "class A run once." << std::endl;
}

bool TaskA::shouldTriggerSinceLast(double duration) const {
    return duration >= 30;
}
```

### BDependency.h
```cpp
#ifndef BDEPENDENCY_H
#define BDEPENDENCY_H

class BDependency {
public:
    BDependency() = default;
    ~BDependency() = default;
};

#endif // BDEPENDENCY_H
```

### TaskB.h
```cpp
#ifndef TASKB_H
#define TASKB_H

#include "Task.h"
#include "BDependency.h"
#include <string>

class TaskB : public Task {
private:
    std::string dbPath;
    BDependency dependency;

public:
    TaskB(const std::string& dbPath, const BDependency& depen);
    void runOnce() override;
    bool shouldTriggerSinceLast(double duration) const override;
};

#endif // TASKB_H
```

### TaskB.cpp
```cpp
#include "TaskB.h"
#include <iostream>

TaskB::TaskB(const std::string& dbPath, const BDependency& depen)
    : dbPath(dbPath), dependency(depen) {}

void TaskB::runOnce() {
    std::cout << "class B run once." << std::endl;
}

bool TaskB::shouldTriggerSinceLast(double duration) const {
    return duration >= 30;
}
```

### MyScheduler.h
```cpp
#ifndef MYSCHEDULER_H
#define MYSCHEDULER_H

#include "BackgroundTaskScheduler.h"
#include "TaskA.h"
#include "TaskB.h"
#include "BDependency.h"
#include <memory>

class MyScheduler : public BackgroundTaskScheduler {
private:
    std::unique_ptr<TaskA> taskA;
    TaskB taskB;

    MyScheduler();

public:
    static MyScheduler& shared();

    void setupToken(const std::string& token);
};

#endif // MYSCHEDULER_H
```

### MyScheduler.cpp
```cpp
#include "MyScheduler.h"

MyScheduler::MyScheduler() : taskB("", BDependency()) {
    registerTask(&taskB, "B");
}

MyScheduler& MyScheduler::shared() {
    static MyScheduler instance;
    return instance;
}

void MyScheduler::setupToken(const std::string& token) {
    if (!taskA) {
        taskA = std::make_unique<TaskA>(token);
        registerTask(taskA.get(), "A");
    }
}
```

### main.cpp
```cpp
#include "MyScheduler.h"

int main() {
    MyScheduler::shared().start();
    if (auto* taskA = MyScheduler::shared().setupToken("new token")) {
        taskA->updateToken("new token");
    }
    return 0;
}
```

In this C++ translation:
- `TaskA` and `TaskB` classes inherit from `Task`, and their functionality is implemented similarly to the Swift version.
- `BackgroundTaskScheduler` provides the core scheduling API.
- `MyScheduler` is implemented as a singleton, with `setupToken` initializing and registering `TaskA`.

# Update #

> You got a mistake, "setupToken" do not has a returned value, so you won't be able to use "auto *task = ".

Thank you for catching that! Here's the corrected `main.cpp` file:

### main.cpp
```cpp
#include "MyScheduler.h"

int main() {
    MyScheduler::shared().start();
    MyScheduler::shared().setupToken("new token");
    if (MyScheduler::shared().taskA) {
        MyScheduler::shared().taskA->updateToken("new token");
    }
    return 0;
}
```

This version calls `setupToken` without expecting a return value and accesses `taskA` directly from the `MyScheduler` singleton instance. Let me know if there’s anything else!