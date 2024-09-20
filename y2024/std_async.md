# Waht is "std::async" and how to use it #

`std::async` is a function template in C++ that runs a function asynchronously, potentially in a separate thread, and returns a `std::future` that holds the result. It can be combined with `std::launch::async` to enforce asynchronous execution, meaning that the function is guaranteed to run on a separate thread.

### Basic Syntax of `std::async`:
```cpp
std::async(std::launch::policy, function, args...);
```
- **`std::launch::async`**: Forces the function to be executed in a separate thread.
- **`std::launch::deferred`**: The function is executed only when the result is explicitly needed (i.e., the future is waited on).
- **`function`**: The function you want to run asynchronously.
- **`args...`**: Arguments for the function.

### Example with `std::launch::async`:

```cpp
#include <iostream>
#include <future>
#include <thread>

int compute(int x) {
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate a time-consuming task
    return x * x;
}

int main() {
    // Launch compute in a separate thread
    std::future<int> result = std::async(std::launch::async, compute, 10);

    std::cout << "Doing other work while compute is running...\n";

    // Wait for the result (blocks until compute finishes)
    int value = result.get();

    std::cout << "Result from async: " << value << std::endl;
    return 0;
}
```

### Explanation:
1. **`std::async(std::launch::async, compute, 10)`**:
   - Launches the `compute` function asynchronously in a new thread, passing `10` as an argument.
   - **`std::launch::async`** ensures that the function will run on a separate thread, rather than deferring its execution until the result is requested.

2. **Main Thread Work**:
   - The main thread continues executing other work while the asynchronous task is running.

3. **Result Handling (`result.get()`)**:
   - The `get()` function of `std::future` blocks until the asynchronous task is finished and returns the result (the squared value of 10 in this case).

### Usage Scenarios:

- **Parallel Execution**: When you need to run independent tasks concurrently, such as network calls, file operations, or complex computations.
- **Concurrency with I/O**: You can perform background tasks while handling other I/O operations on the main thread.
  
### Launch Policies:
1. **`std::launch::async`**:
   - Forces the function to run asynchronously in a new thread.
   - Guarantees concurrent execution.
   
2. **`std::launch::deferred`**:
   - The function is only executed when its result is requested (e.g., via `future.get()` or `future.wait()`).
   - No separate thread is created unless the result is explicitly needed.

3. **Default Behavior**:
   If you don't specify a launch policy, the system can decide between `std::launch::async` and `std::launch::deferred` based on resource availability.

### Example with Deferred Execution (`std::launch::deferred`):

```cpp
#include <iostream>
#include <future>

int compute(int x) {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return x * x;
}

int main() {
    // Launch compute with deferred policy (no new thread until result is needed)
    std::future<int> result = std::async(std::launch::deferred, compute, 10);

    std::cout << "Doing other work...\n";

    // Explicitly invoke compute and wait for result
    int value = result.get();

    std::cout << "Result from deferred async: " << value << std::endl;
    return 0;
}
```
In this case, the `compute` function only runs when the `result.get()` call is made, and no thread is created unless the result is needed.

### Combining `std::async` with Timed Waiting:

If you want to wait for an asynchronous result for a specific amount of time, you can use `std::future::wait_for` or `std::future::wait_until`.

```cpp
#include <iostream>
#include <future>
#include <chrono>

int compute(int x) {
    std::this_thread::sleep_for(std::chrono::seconds(3));
    return x * x;
}

int main() {
    std::future<int> result = std::async(std::launch::async, compute, 10);

    // Wait for up to 2 seconds for the result
    if (result.wait_for(std::chrono::seconds(2)) == std::future_status::ready) {
        std::cout << "Result: " << result.get() << std::endl;
    } else {
        std::cout << "Timeout: computation is still running" << std::endl;
    }

    return 0;
}
```

### Key Points:
1. **`std::async`** with `std::launch::async` ensures concurrent execution by launching the function in a separate thread.
2. **`std::launch::deferred`** delays execution until the result is needed.
3. **`std::future`** is used to retrieve the result of the asynchronous operation, blocking the calling thread if necessary.

Would you like to dive deeper into how to manage multiple `std::future` objects or further details about exception handling with `std::async`?