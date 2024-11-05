# Super and subclass initializer #

```
Translate following code from Swift to C++, and create a separated header for each class:

class Foo {
    let price: String
    init(thePrice: String) {
        price = thePrice
    }
    func doSomthing() {
        print("Hello")
    }
}

class Bar {
    let age: Int
    init(theAge: Int) {
        age = theAge
    }
    func getUp() {
        print("Hello")
    }
}


class Base {
    let name: String
    let theFoo: Foo

    init(myName: String) {
        name = myName
        theFoo = Foo(thePrice: myName)
    }

    func baseMethoid() {
        print("Hello")
    }
}

class Business: Base {
    let theOther: String
    let theBar: Bar
    init(myName: String, other: String, myAge: Int) {
        theOther = other
        theBar = Bar(theAge: myAge)
        super.init(myName: myName)
    }
    func biziMethoid() {
        print("Hello")
    }
}
```

Here’s the translation of the Swift code into C++ with each class placed in a separate header file, implementing both data members and functions.

### `Foo.h`

```cpp
#ifndef FOO_H
#define FOO_H

#include <string>
#include <iostream>

class Foo {
public:
    std::string price;

    // Constructor
    Foo(const std::string& thePrice);

    // Member function
    void doSomething() const;
};

#endif // FOO_H
```

### `Foo.cpp`

```cpp
#include "Foo.h"

Foo::Foo(const std::string& thePrice) : price(thePrice) {}

void Foo::doSomething() const {
    std::cout << "Hello" << std::endl;
}
```

---

### `Bar.h`

```cpp
#ifndef BAR_H
#define BAR_H

#include <iostream>

class Bar {
public:
    int age;

    // Constructor
    Bar(int theAge);

    // Member function
    void getUp() const;
};

#endif // BAR_H
```

### `Bar.cpp`

```cpp
#include "Bar.h"

Bar::Bar(int theAge) : age(theAge) {}

void Bar::getUp() const {
    std::cout << "Hello" << std::endl;
}
```

---

### `Base.h`

```cpp
#ifndef BASE_H
#define BASE_H

#include <string>
#include <iostream>
#include "Foo.h"

class Base {
public:
    std::string name;
    Foo theFoo;

    // Constructor
    Base(const std::string& myName);

    // Member function
    void baseMethod() const;
};

#endif // BASE_H
```

### `Base.cpp`

```cpp
#include "Base.h"

Base::Base(const std::string& myName) : name(myName), theFoo(myName) {}

void Base::baseMethod() const {
    std::cout << "Hello" << std::endl;
}
```

---

### `Business.h`

```cpp
#ifndef BUSINESS_H
#define BUSINESS_H

#include <string>
#include <iostream>
#include "Base.h"
#include "Bar.h"

class Business : public Base {
public:
    std::string theOther;
    Bar theBar;

    // Constructor
    Business(const std::string& myName, const std::string& other, int myAge);

    // Member function
    void biziMethod() const;
};

#endif // BUSINESS_H
```

### `Business.cpp`

```cpp
#include "Business.h"

Business::Business(const std::string& myName, const std::string& other, int myAge)
    : Base(myName), theOther(other), theBar(myAge) {}

void Business::biziMethod() const {
    std::cout << "Hello" << std::endl;
}
```

### Explanation:

1. **Header Guards**: Each header file uses `#ifndef`, `#define`, and `#endif` to prevent multiple inclusions.
2. **Constructor Implementations**: Each class has its own `.cpp` file, which contains constructor and method implementations.
3. **Function Implementation**: The functions `doSomething()`, `getUp()`, `baseMethod()`, and `biziMethod()` are defined in their respective `.cpp` files, using `std::cout` to print `"Hello"` to match the `print("Hello")` in Swift.

