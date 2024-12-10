# CMakeLists execute order

> That looks like you just put it in order, and it will take effect when "add_library()" statement appears, is that true?

Yes, you're correct! In CMake, the order of commands and their association with specific targets is crucial. Here's a detailed explanation of how it works in relation to your question:

---

### **How CMake Commands Take Effect**

1. **Global Variables or Options (like `set()` or `option()`)**  
   These commands define global settings and will affect everything *after* they are set, **unless overridden for a specific target**. For example:  

   ```cmake
   set(PLATFORM OS64 CACHE STRING "Platform to compile for")
   ```

   This value is globally available and will affect any subsequent `add_library()` or `add_executable()` commands *unless* they specify a different value.

2. **Target-Specific Properties (like `target_compile_definitions()`)**  
   These commands only affect the specific target they're associated with. For example:

   ```cmake
   add_library(marian_iphone STATIC ...)
   target_compile_definitions(marian_iphone PRIVATE PLATFORM=OS64)
   ```

   This will set `PLATFORM=OS64` for **only the `marian_iphone` target**, even if the global `PLATFORM` variable is set differently.

3. **Order of Execution Matters**  
   Commands like `set()` or `add_library()` are processed in the order they appear. For example:

   ```cmake
   set(PLATFORM OS64 CACHE STRING "Platform to compile for")
   add_library(marian_iphone STATIC ...)
   set(PLATFORM android CACHE STRING "Platform to compile for")
   add_library(marian_android STATIC ...)
   ```

   In this case:
   - The `marian_iphone` target will use `PLATFORM=OS64` because that value was set before it was added.
   - The `marian_android` target will use `PLATFORM=android` because the value was updated before adding the second target.

---

### **Why Target-Specific Commands are Preferred**
If you rely on global variables (`set()`), it can be easy to accidentally apply incorrect settings to multiple targets. Using target-specific commands (`target_compile_definitions()` or `target_include_directories()`) ensures the settings are explicitly tied to the intended target and won't unintentionally "spill over."

For example:
```cmake
add_library(marian_iphone STATIC ...)
target_compile_definitions(marian_iphone PRIVATE PLATFORM=OS64)

add_library(marian_android STATIC ...)
target_compile_definitions(marian_android PRIVATE PLATFORM=android)
```

This approach guarantees the `PLATFORM` definition is correctly set for each target, independent of the global order.

---

### **Conclusion**
Your observation is correct: **CMake commands take effect when they are encountered**, so the value of `PLATFORM` (or any other setting) depends on what was defined at the point the `add_library()` or `add_executable()` command is called. To avoid unexpected behavior, it’s a good practice to use target-specific properties instead of relying on global variables when dealing with multiple targets.
