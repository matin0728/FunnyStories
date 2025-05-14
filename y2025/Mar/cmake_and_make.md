# Cmake and make tool #

> what's the difference between "cmake" and "make" command?

The **`cmake`** and **`make`** commands are distinct tools used in the process of building software, and they serve different purposes in a typical build workflow. Here's how they differ:

---

### **1. `cmake`**
- **Purpose**: `cmake` is a **build system generator**.
- **Role**: It is responsible for generating platform-specific build files (e.g., Makefiles, Visual Studio projects, Ninja build scripts) from a high-level description in `CMakeLists.txt`.

#### Key Characteristics:
- **Input**: `CMakeLists.txt` files, which define the structure of the project, including source files, targets (e.g., executables, libraries), dependencies, and build options.
- **Output**: 
  - Generates build system files appropriate for the platform and build toolchain. For example:
    - On Linux: Makefiles (default).
    - On Windows: Visual Studio solution files or Ninja scripts.
    - On macOS: Xcode projects.
- **Cross-Platform**: Works across multiple platforms and integrates with different build tools.
- **Usage**:
  - Initial configuration step:
    ```bash
    cmake -S <source_dir> -B <build_dir> -G "Unix Makefiles"
    ```
    This generates Makefiles in the `<build_dir>` based on the project's `CMakeLists.txt`.

---

### **2. `make`**
- **Purpose**: `make` is a **build tool**.
- **Role**: It is responsible for executing the build process using instructions provided in a `Makefile` or other generated build script.

#### Key Characteristics:
- **Input**: A `Makefile`, which defines rules for compiling and linking files, including dependencies between files.
- **Output**: Builds the project by compiling source files and linking them to produce the final binary (e.g., an executable or library).
- **Dependency Tracking**: Ensures only modified files (or files affected by changes) are rebuilt, making the build process efficient.
- **Platform-Specific**: Works primarily on Unix-like systems (Linux, macOS).

---

### **Workflow Relationship**:
1. **`cmake` comes first**:
   - Use `cmake` to generate the `Makefile` from your project’s `CMakeLists.txt`.
   - Example:
     ```bash
     cmake -S . -B build
     ```
     This creates the `Makefile` in the `build` directory.

2. **`make` comes next**:
   - Use `make` to build the project using the generated `Makefile`.
   - Example:
     ```bash
     make -C build
     ```
     This compiles the code and creates the output (e.g., executable or library).

---

### **Comparison Table**:

| **Feature**            | **CMake**                           | **Make**                       |
|-------------------------|-------------------------------------|--------------------------------|
| **Purpose**            | Generates build files (e.g., Makefiles, Ninja) | Executes the build process based on a Makefile |
| **Input**              | `CMakeLists.txt`                   | `Makefile`                    |
| **Output**             | Makefiles, Ninja scripts, Visual Studio projects, etc. | Compiled binaries, libraries, or executables |
| **Cross-Platform**     | Yes                                | Limited (primarily Unix/Linux) |
| **Dependency Tracking**| No                                 | Yes (within the `Makefile`)    |
| **Usage**              | Configure/build system generation  | Actual build execution         |

---

### **Summary**:
- **`cmake`**: Prepares the build by generating the required build files.
- **`make`**: Executes the actual build process based on those files.

In projects that use CMake, you typically run `cmake` first to generate the necessary build files, and then use `make` (or another build tool) to compile the project.
