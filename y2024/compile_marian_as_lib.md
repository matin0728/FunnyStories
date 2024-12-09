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


# Step 2

> If "marian" requires "yaml-cpp", will it be automatically linked in within the artifact?

No, Marian will not automatically include **`yaml-cpp`** in the final static library unless explicitly linked during the build process. Even if Marian depends on `yaml-cpp`, you need to ensure that it is properly configured in your CMake build to include the required libraries in the final static artifact.

Here's how to ensure that **`yaml-cpp`** is correctly linked in the build process:

---

### 1. **Check Marian's CMake Configuration**
The `CMakeLists.txt` file in Marian's source code should include logic for linking its dependencies, including `yaml-cpp`. However, this does not guarantee that Marian's `yaml-cpp` dependency will be transitively included in your final library.

---

### 2. **Ensure `yaml-cpp` is Available**
1. **Install `yaml-cpp`**:
   Install `yaml-cpp` on your system if it's not included as part of the Marian repository.

   - **Install via Homebrew**:
     ```bash
     brew install yaml-cpp
     ```
   - **Build Manually** (if needed):
     Clone and build `yaml-cpp` manually to get a static library:
     ```bash
     git clone https://github.com/jbeder/yaml-cpp.git
     cd yaml-cpp
     mkdir build && cd build
     cmake .. -DBUILD_SHARED_LIBS=OFF
     make
     ```

2. **Ensure Marian Detects `yaml-cpp`**:
   Marian's `CMakeLists.txt` should automatically find `yaml-cpp` if it is installed on your system. Marian typically uses `find_package(yaml-cpp)` in its CMake configuration to locate the library. Ensure `yaml-cpp` is in your system's library paths (`/usr/local/lib` or `CMAKE_PREFIX_PATH`).

   - If `yaml-cpp` is not detected, you can specify its path:
     ```bash
     cmake .. -Dyaml-cpp_DIR=/path/to/yaml-cpp/cmake
     ```

---

### 3. **Link `yaml-cpp` Manually (if Needed)**
If Marian does not automatically link `yaml-cpp`, you can explicitly link it in your project's `CMakeLists.txt`.

#### Updated `CMakeLists.txt` Example:
```cmake
# Marian and yaml-cpp setup
add_subdirectory(external/marian)
find_package(yaml-cpp REQUIRED)

# Add your static library
add_library(your_static_lib STATIC src/your_library.cpp)

# Link Marian and yaml-cpp explicitly
target_link_libraries(your_static_lib PUBLIC marian yaml-cpp)
target_include_directories(your_static_lib PUBLIC
    external/marian/src
    ${yaml-cpp_INCLUDE_DIRS}
)
```

---

### 4. **Verify Linking in the Final Artifact**
To confirm that `yaml-cpp` symbols are included in your final library:

1. **Inspect the Static Library (`libyour_static_lib.a`)**:
   Use `nm` to check if `yaml-cpp` symbols (e.g., `YAML::InvalidNode`) are present:
   ```bash
   nm -g libyour_static_lib.a | grep YAML
   ```

2. **Check Dependencies**:
   Ensure that `yaml-cpp` is properly linked by Marian in its static library:
   ```bash
   nm -g external/marian/libmarian.a | grep YAML
   ```

---

### 5. **Build and Test**
Rebuild your project to include Marian and `yaml-cpp`:

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64
make
```

After the build, your static library (`libyour_static_lib.a`) should include both Marian and `yaml-cpp`.

---

### 6. **Distribute the Final Artifact**
The resulting `libyour_static_lib.a` will now contain both Marian and `yaml-cpp`. You can use this single static library in your iOS project without separately managing `yaml-cpp`.

Let me know if you face any challenges during the process!


# Step 3

> If I skip this step, can I merge "yaml-cpp" into the lib "libyour_static_lib.a" that built without "yaml-cpp"?

Yes, if you skip explicitly linking **`yaml-cpp`** during the build process of `libyour_static_lib.a`, you can still merge `yaml-cpp` with your library afterward to include its symbols. This involves combining the two static libraries (`libyour_static_lib.a` and `libyaml-cpp.a`) into a single static library.

Here's how you can do it:

---

### Steps to Merge `libyour_static_lib.a` with `libyaml-cpp.a`

#### 1. **Ensure Architecture Compatibility**
Ensure that both static libraries are compiled for the same architecture (e.g., `arm64`). Use the `lipo` command to verify this:

```bash
lipo -info libyour_static_lib.a
lipo -info libyaml-cpp.a
```

If the architectures do not match, you need to rebuild one or both libraries to ensure compatibility.

---

#### 2. **Merge Libraries Using `libtool`**
You can combine the two static libraries into one using the `libtool` command:

```bash
libtool -static -o libfinal.a libyour_static_lib.a libyaml-cpp.a
```

- `-static`: Specifies that you are creating a static library.
- `-o libfinal.a`: The name of the output merged static library.
- `libyour_static_lib.a libyaml-cpp.a`: The input static libraries.

This will create a new static library (`libfinal.a`) that contains the symbols from both `libyour_static_lib.a` and `libyaml-cpp.a`.

---

#### 3. **Verify the Merged Library**
After merging, ensure that the required symbols are included:

1. **Inspect the Symbols**
   Use `nm` to list the symbols in the merged library and verify that the `yaml-cpp` symbols are present:
   ```bash
   nm -g libfinal.a | grep YAML
   ```

2. **Check for Architecture**
   Confirm the architecture of the merged library:
   ```bash
   lipo -info libfinal.a
   ```

---

#### 4. **Use the Merged Library**
Replace `libyour_static_lib.a` and `libyaml-cpp.a` in your iOS project with the new `libfinal.a`. Link this library in your Xcode project under **Build Phases > Link Binary with Libraries**.

---

### Notes

1. **Potential Duplicate Symbols**
   If Marian and `yaml-cpp` share overlapping symbols or dependencies, you might encounter duplicate symbol errors during linking. To resolve this:
   - Use `strip` to remove unused symbols from individual libraries before merging.
   - Remove symbols explicitly with `ar` (requires advanced handling).

   Example to remove unused symbols:
   ```bash
   strip -S libyaml-cpp.a
   ```

2. **Order of Linking**
   When merging libraries, the order matters if there are unresolved dependencies. Always place dependent libraries (e.g., `libyaml-cpp.a`) after the library that depends on them (e.g., `libyour_static_lib.a`).

3. **Debugging Missing Symbols**
   If you still encounter missing symbols at runtime, check which library defines the missing symbol:
   ```bash
   nm -g libyaml-cpp.a | grep <missing-symbol-name>
   ```

---

By merging `yaml-cpp` with your static library after the build, you avoid the need to explicitly link it during the initial build process, but you still ensure all required symbols are included for distribution. Let me know if you need help with any of these steps!
