# Can I use generic types in C++ just like in Swift? #

Yes, C++ has a feature called *templates* that allows you to create generic types, similar to Swift's generics. Templates enable you to write flexible and reusable code that can work with different data types. 

Here’s a comparison of how generics work in Swift and templates in C++:

### Generic Example in Swift
```swift
struct Stack<T> {
    private var elements: [T] = []
    
    mutating func push(_ element: T) {
        elements.append(element)
    }
    
    mutating func pop() -> T? {
        return elements.popLast()
    }
}
```

### Template Example in C++
```cpp
template <typename T>
class Stack {
private:
    std::vector<T> elements;

public:
    void push(const T& element) {
        elements.push_back(element);
    }
    
    T pop() {
        if (elements.empty()) {
            throw std::out_of_range("Stack is empty");
        }
        T element = elements.back();
        elements.pop_back();
        return element;
    }
};
```

### Explanation
- **Swift Generics (`<T>`):** Swift uses the syntax `<T>` to define a generic type. It allows the `Stack` to work with any type, whether it's an `Int`, `String`, or a custom object.
  
- **C++ Templates (`template <typename T>`):** In C++, you use `template <typename T>` to define a class or function that can accept any type. `T` serves as a placeholder, which is replaced by the actual type when the template is instantiated.

Both approaches allow you to write a class or function once and reuse it with different data types. However, C++ templates are more powerful and flexible than Swift generics because they support not only types but also non-type parameters (like integers) and template specialization, which allows for different implementations based on specific types or conditions.