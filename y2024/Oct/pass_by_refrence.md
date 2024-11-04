# Why and when we will pass by refrence? #

The `&` symbol in `std::vector<Event>& events` indicates that the parameter is being passed by **reference** rather than by **value**. Here's why passing by reference is important:

1. **Avoiding Copying**: If you pass the `events` vector by value (i.e., without `&`), a **copy** of the vector would be made every time the function is called. Copying a vector can be costly, especially if the vector is large, because it duplicates the entire contents of the vector.

2. **Efficiency**: By passing the vector by reference (`&`), the function operates directly on the original vector without making a copy. This saves both time and memory, improving the efficiency of the function.

3. **Modifications (if needed)**: If the function needs to modify the contents of the vector, passing by reference ensures that the original vector is modified, not a copy. Even though in this case, the function isn't modifying the vector, passing by reference is still preferred to avoid the unnecessary overhead of copying.

### Example:

```cpp
void processVector(std::vector<Event>& events) {
    // This function works with the original 'events' vector
}

void processVectorByValue(std::vector<Event> events) {
    // This function works with a copy of 'events', potentially costly
}
```

In the first function (`processVector`), the original vector is used, avoiding the overhead of copying, whereas in the second function (`processVectorByValue`), a copy of the vector is created, which can be inefficient.

Since the `upload` method in your `UploadManager` class doesn't modify the vector, passing it by `const std::vector<Event>&` would also work, making it clear that the function won't modify the input:

```cpp
void upload(const std::vector<Event>& events, Callback callback);
```

This would enforce that the vector is only read, not changed.