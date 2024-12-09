# Compile Marian as static lib #

> I need create a repo to compile the lib "marian", which is a source lib and can be compile using CMake, 
> I create a submodule to it, and then how can I do the rest job to build a static lib with arm64 architecture, using the "marian" lib as dependency?

To create a repository that builds a static library using the **Marian** library as a dependency with `arm64` architecture, follow these steps:

---

### 1. **Set Up Your Repository**
1. **Initialize a New Git Repository**
   ```bash
   git init marian-static-lib
   cd marian-static-lib
   ```

2. **Add Marian as a Submodule**
   ```bash
   git submodule add https://github.com/marian-nmt/marian-dev.git external/marian
   git submodule update --init --recursive
   ```

3. **Create a CMake Project**
   Add a `CMakeLists.txt` to your repository root:

   ```plaintext
   marian-static-lib/
   ├── CMakeLists.txt
   ├── external/
   │   └── marian/  # Marian submodule
   └── src/
       └── your_library.cpp
   ```

---

### 2. **Write the `CMakeLists.txt`**
Configure the build system to use Marian as a dependency and generate an ARM64 static library.

#### **Top-Level `CMakeLists.txt`**
```cmake
cmake_minimum_required(VERSION 3.15)
project(MarianStaticLib)

# Set architecture to ARM64
set(CMAKE_OSX_ARCHITECTURES "arm64")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set the output directory for built libraries
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Add Marian submodule
add_subdirectory(external/marian)

# Add your source files
add_library(your_static_lib STATIC src/your_library.cpp)

# Link Marian to your static library
target_link_libraries(your_static_lib PUBLIC marian)
target_include_directories(your_static_lib PUBLIC external/marian/src)
```

#### **`src/your_library.cpp`**
Create your own source file for testing:

```cpp
#include "marian.h" // Example include from Marian

void your_function() {
    // Use Marian library here
}
```

---

### 3. **Build the Static Library**

#### **Step 1: Create a Build Directory**
Keep the build files out of the source tree:
```bash
mkdir build && cd build
```

#### **Step 2: Configure the Build with CMake**
Run CMake to generate build files for ARM64:
```bash
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64
```

#### **Step 3: Compile the Static Library**
```bash
make
```

This will:
- Build the Marian library.
- Compile your static library (`libyour_static_lib.a`) with ARM64 architecture.

The resulting static library will be located in `build/lib/`.

---

### 4. **Verify the Static Library**

1. **Check the Architectures**
   Use `lipo` to confirm it is compiled for `arm64`:
   ```bash
   lipo -info libyour_static_lib.a
   ```

2. **Inspect Symbols**
   Use `nm` to ensure Marian's symbols are included:
   ```bash
   nm -g libyour_static_lib.a | grep marian
   ```

---

### 5. **Troubleshooting Tips**

1. **Missing Dependencies**
   Marian may require external dependencies like `zlib` or `boost`. Install them via Homebrew:
   ```bash
   brew install boost zlib
   ```

2. **Compiler Issues**
   If you encounter compilation errors, ensure you're using a compatible compiler:
   ```bash
   export CC=/usr/bin/clang
   export CXX=/usr/bin/clang++
   ```

3. **Debugging Submodule Issues**
   If Marian fails to build, ensure the submodule is up to date:
   ```bash
   git submodule update --init --recursive
   ```

---

### 6. **Distribute the Static Library**
Once built, you can copy `libyour_static_lib.a` into your iOS project and link it in Xcode, ensuring you set the architecture to `arm64`.

---

Let me know if you encounter any issues or need additional guidance!
