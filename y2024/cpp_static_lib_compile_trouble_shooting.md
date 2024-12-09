# Cpp static lib compile trouble shooting #

> I have compiled a lib written in C++ into a static lib and add to my iOS project, then I copy all of its header file into my project also, 
> after that, when I compile the project, the compiler reports that a lot of missing symbols,
> e.g: "Undefined symbol: YAML::InvalidNode::~InvalidNode()", did I missing something?

The "undefined symbol" error indicates that the linker cannot find the implementation for the symbol in question, which suggests an issue with how the static library and its dependencies are integrated into your project. Here are the most common causes and solutions:

---

### 1. **Missing Implementation in the Static Library**
   - The symbol `YAML::InvalidNode::~InvalidNode()` suggests you're using a library (e.g., `yaml-cpp`) that hasn't been properly linked.
   - **Solution**: Verify that the `yaml-cpp` symbols were included in the static library during the compilation process. If you're using `yaml-cpp`, ensure it was compiled and linked correctly into your static library.

---

### 2. **Static Library Dependencies**
   - If your static library relies on other libraries (e.g., `yaml-cpp`), you need to link those dependent libraries explicitly.
   - **Solution**: Add the dependent libraries (e.g., `libyaml-cpp.a`) to your Xcode project's "Link Binary with Libraries" section or in your `OTHER_LDFLAGS`.

---

### 3. **Header and Library Mismatch**
   - Ensure the header files you copied match the version of the compiled static library. Mismatches can cause symbols to be missing.
   - **Solution**: Use the exact same headers used to compile the static library. If you're compiling `yaml-cpp` yourself, include its headers alongside the library.

---

### 4. **Linker Flags**
   - If the library uses C++ features (as suggested by the `YAML::` namespace), you may need to explicitly tell the linker to link against the C++ standard library.
   - **Solution**: Add `-lc++` or `-lstdc++` to your `OTHER_LDFLAGS` in Xcode, depending on which standard library was used when the static library was compiled.

---

### 5. **Architecture Mismatch**
   - If the static library was compiled for a different architecture than your iOS project, you'll get undefined symbol errors.
   - **Solution**: Confirm that the static library is compiled for the same architectures as your Xcode project's target (e.g., `arm64`, `x86_64` for simulators). Use the `lipo` command to inspect the library's architectures:
     ```bash
     lipo -info libyourlibrary.a
     ```

---

### 6. **Verify the Static Library Contents**
   - Sometimes, the static library does not include all required symbols.
   - **Solution**: Use `nm` to inspect the static library and confirm it contains the missing symbol (`YAML::InvalidNode::~InvalidNode()`):
     ```bash
     nm -g libyourlibrary.a | grep InvalidNode
     ```

---

### 7. **Rebuild the Static Library**
   - If the issue persists, consider rebuilding the static library with all dependencies included and double-check the build process.
   - **Solution**: Compile the library with a command that ensures all symbols are linked:
     ```bash
     g++ -o libyourlibrary.a source1.cpp source2.cpp -lyaml-cpp -static
     ```

---

### Debugging Steps
1. Ensure the static library includes the required symbols.
2. Add the dependent libraries explicitly to Xcode.
3. Check for architecture mismatches.
4. Include the necessary C++ standard libraries (`-lc++`).
5. Confirm that all header files match the static library version.

Let me know if you need help with specific commands or Xcode configurations!
