# What is std::contidition_variable and how to use it? #

`std::condition_variable` is a synchronization primitive in C++ that allows threads to communicate with each other by sending notifications. It is commonly used in scenarios where one or more threads need to wait for a specific condition to become true before proceeding.

### Key Concepts:
- **Waiting**: A thread can wait on a `std::condition_variable` until another thread notifies it.
- **Notification**: Another thread can signal the waiting thread using `notify_one()` or `notify_all()` when the condition is met.
- **Mutex**: `std::condition_variable` is usually used with a `std::mutex` to ensure that the condition is checked and modified safely in a multithreaded environment.

### Basic Workflow:
1. A thread waits on the condition variable (often in a loop) until a certain condition is true.
2. Another thread changes the condition and notifies the waiting thread by calling `notify_one()` (for one thread) or `notify_all()` (for all waiting threads).

### How to Use `std::condition_variable`:

Here is an example illustrating how to use `std::condition_variable` for thread synchronization:

### Example: Producer-Consumer Problem

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>

std::mutex mtx;                           // Mutex for critical section
std::condition_variable cv;                // Condition variable for communication
std::queue<int> dataQueue;                 // Shared data
bool finished = false;                     // Flag to signal when production is done

// Producer: produces data and notifies the consumer
void producer() {
    for (int i = 0; i < 5; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(500));  // Simulate work
        std::lock_guard<std::mutex> lock(mtx);                        // Lock mutex
        dataQueue.push(i);                                            // Add data to queue
        std::cout << "Produced: " << i << std::endl;
        cv.notify_one();                                              // Notify consumer
    }

    // Notify consumer that production is finished
    {
        std::lock_guard<std::mutex> lock(mtx);
        finished = true;
    }
    cv.notify_one();
}

// Consumer: waits for data and processes it
void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return !dataQueue.empty() || finished; });  // Wait until data is available or finished

        // Process all data in the queue
        while (!dataQueue.empty()) {
            int value = dataQueue.front();
            dataQueue.pop();
            std::cout << "Consumed: " << value << std::endl;
        }

        // Exit when production is finished
        if (finished) break;
    }
}

int main() {
    std::thread producerThread(producer);
    std::thread consumerThread(consumer);

    producerThread.join();
    consumerThread.join();

    return 0;
}
```

### Explanation:
1. **Mutex (`std::mutex`)**: Guards access to the shared data (`dataQueue`) to prevent race conditions.
2. **Condition Variable (`std::condition_variable`)**: Used to notify the consumer thread when data is available or production is finished.
3. **Producer**: The producer generates data and notifies the consumer every time new data is added to the queue. After producing all items, it sets the `finished` flag and notifies the consumer.
4. **Consumer**: The consumer waits on the condition variable (`cv.wait`) until either data is available or production is finished. Once it receives the notification, it processes the data.

### Key Functions of `std::condition_variable`:
- **`wait`**:
   - `cv.wait(lock)` suspends the current thread until the condition variable is notified. It releases the lock on the mutex while waiting, and re-acquires it after waking up.
   - A predicate can be passed to `wait` to avoid spurious wakeups:
     ```cpp
     cv.wait(lock, []{ return condition; });
     ```
- **`notify_one()`**: Wakes up one of the threads waiting on the condition variable.
- **`notify_all()`**: Wakes up all threads waiting on the condition variable.

### Why Use `std::condition_variable`?
- **Efficient Waiting**: Threads can sleep while waiting for a condition, conserving CPU cycles.
- **Thread Communication**: Threads can be synchronized to react when certain conditions are met.
  
### Example Use Cases:
- Producer-consumer problem.
- Task scheduling (e.g., running tasks at intervals).
- Thread-safe resource pools where threads wait for resources to become available.

### Important Notes:
- `std::condition_variable` must always be used with a `std::mutex` to protect shared data.
- When a thread wakes up, it may not be guaranteed that the condition is satisfied (due to spurious wakeups). This is why it’s common to use a `while` loop or pass a predicate to the `wait` method.