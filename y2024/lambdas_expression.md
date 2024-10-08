# Lambdas expression #

A **lambda expression** (or **lambda function**) in C++ is a concise way to define an anonymous function that can be defined in the scope of your code. Lambdas are particularly useful for creating short, throwaway functions that you want to pass as arguments to algorithms or functions, such as with `std::for_each`, `std::sort`, etc. 

### Key Features of Lambda Expressions:

1. **Anonymous Function**: Lambdas are functions without a name. They are defined in place and are typically used for short-lived operations.

2. **Syntax**:
   The general syntax for a lambda expression in C++ is as follows:
   ```cpp
   [capture_list](parameters) -> return_type {
       // function body
   }
   ```

   - **Capture List**: This is specified in square brackets (`[]`) and determines which variables from the surrounding scope can be accessed within the lambda. You can capture by value or by reference.
   - **Parameters**: This is similar to regular function parameters, defined in parentheses.
   - **Return Type**: This is optional and can be specified after the parameters using the arrow (`->`) syntax. If omitted, C++ will attempt to deduce the return type.
   - **Function Body**: This contains the statements that make up the body of the lambda.

3. **Example**:
   Here’s a simple example demonstrating a lambda expression:

   ```cpp
   #include <iostream>
   #include <vector>
   #include <algorithm>

   int main() {
       std::vector<int> numbers = {1, 2, 3, 4, 5};

       // Lambda to print each number
       auto print = [](int value) {
           std::cout << value << " ";
       };

       std::cout << "Numbers: ";
       std::for_each(numbers.begin(), numbers.end(), print);
       std::cout << std::endl;

       // Lambda to calculate the sum of the numbers
       int sum = 0;
       std::for_each(numbers.begin(), numbers.end(), [&sum](int value) {
           sum += value; // Capture sum by reference
       });

       std::cout << "Sum: " << sum << std::endl;

       return 0;
   }
   ```

### Explanation of the Example:
- **Printing with Lambda**: 
  - The `print` lambda is defined to take an `int` and print it. It is then passed to `std::for_each`, which iterates over `numbers` and applies the lambda to each element.
  
- **Capturing Variables**: 
  - The second lambda captures the `sum` variable by reference (`&sum`), allowing it to modify the `sum` variable defined outside the lambda scope. 

### Benefits of Lambda Expressions:
- **Conciseness**: They allow for shorter and more readable code by avoiding the need to define a separate named function.
- **Flexibility**: Lambdas can capture variables from their surrounding scope, making them powerful for callback functions.
- **Ease of Use with STL**: They integrate seamlessly with the C++ Standard Library, especially with algorithms in `<algorithm>`.

### C++ Version Support:
Lambda expressions were introduced in C++11 and have become an integral part of modern C++ programming, with additional features and enhancements in subsequent standards (C++14, C++17, C++20).

### Conclusion:
In summary, lambda expressions in C++ provide a powerful and flexible way to define anonymous functions for use in algorithms and other scenarios where a short function definition is needed. They enhance code readability and allow for functional-style programming within C++.