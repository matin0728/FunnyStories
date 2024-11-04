# Singleton patten and property initializer #

I have 2 classes, give the code written with C++ based on descriptioins:

- Class "Foo", follow a singleton pattern, and the shared instance should be initialized only once using a string parameter: "path" by a static method: "configure", and it return the shared instance by method: "getInstance", it also has an instance field which is an instance of class "Bar", the instance should be initialized in the constructor using the param "path" passed in.

- Class "Bar": Has a instance field "path", should be initialized by constructor, another method call "fetch", which returns an int number.
  

# Response #

Here’s the updated implementation based on the new requirements where `Foo` now has an instance of another class `Zoo`, which takes no parameters in its constructor.

### `Zoo.hpp` (Header file)

```cpp
#ifndef ZOO_HPP
#define ZOO_HPP

class Zoo {
public:
    // Constructor with no parameters
    Zoo();

    // Example method
    void doSomething();
};

#endif // ZOO_HPP
```

### `Zoo.cpp` (Implementation file)

```cpp
#include "Zoo.hpp"
#include <iostream>

// Constructor with no parameters
Zoo::Zoo() {
    // Constructor logic, if any
}

// Example method
void Zoo::doSomething() {
    std::cout << "Zoo is doing something!" << std::endl;
}
```

---

### Updated `Foo.hpp` (Header file)

```cpp
#ifndef FOO_HPP
#define FOO_HPP

#include <memory>
#include "Bar.hpp"
#include "Zoo.hpp"

class Foo {
private:
    static std::unique_ptr<Foo> instance;  // Static unique instance of Foo
    Bar bar;  // Instance of class Bar
    Zoo zoo;  // Instance of class Zoo

    // Private constructor to prevent instantiation from outside
    Foo(const std::string& path);

public:
    // Method to configure the singleton with the path and initialize if not already done
    static void configure(const std::string& path);

    // Method to get the shared instance of Foo
    static Foo* getInstance();

    // Method to access the Bar instance
    Bar& getBar();

    // Method to access the Zoo instance
    Zoo& getZoo();
};

#endif // FOO_HPP
```

### Updated `Foo.cpp` (Implementation file)

```cpp
#include "Foo.hpp"
#include <stdexcept>

// Initialize the static instance to nullptr
std::unique_ptr<Foo> Foo::instance = nullptr;

// Private constructor to initialize "bar" with the given path and "zoo" without parameters
Foo::Foo(const std::string& path) : bar(path), zoo() {}

// Static method to configure the singleton with the path
void Foo::configure(const std::string& path) {
    if (!instance) {
        instance = std::make_unique<Foo>(path);
    }
}

// Static method to get the shared instance of Foo
Foo* Foo::getInstance() {
    if (!instance) {
        throw std::runtime_error("Foo is not configured. Call configure() first.");
    }
    return instance.get();
}

// Method to access the Bar instance
Bar& Foo::getBar() {
    return bar;
}

// Method to access the Zoo instance
Zoo& Foo::getZoo() {
    return zoo;
}
```

---

### Updated `main.cpp` (Example Usage)

```cpp
#include "Foo.hpp"
#include <iostream>

int main() {
    // Configure the Foo singleton
    Foo::configure("/path/to/resource");

    // Get the shared instance
    Foo* foo = Foo::getInstance();

    // Use the Bar instance
    int result = foo->getBar().fetch();
    std::cout << "Fetched value from Bar: " << result << std::endl;

    // Use the Zoo instance
    foo->getZoo().doSomething();

    return 0;
}
```

### Key Changes:
1. **Class `Zoo`**: A new class with a no-parameter constructor and a simple method `doSomething` as an example.
2. **Class `Foo`**: Now includes an instance of `Zoo`, initialized without parameters in the constructor.
3. **`main.cpp`**: Now demonstrates accessing both `Bar` and `Zoo` instances from `Foo`.