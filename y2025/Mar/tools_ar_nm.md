# what is the tools ar and nm? #

`ar` and `nm` are command-line tools commonly used in development to work with static libraries and inspect symbols in object files or libraries. Here's an explanation of each:

---

### 1. **`ar` (Archiver)**

`ar` stands for **archiver**. It is used to create, modify, and extract contents from static library files (`.a` files), which are collections of compiled object files (`.o`).

#### Common Use Cases:
- **Create a static library**: Combine multiple object files into a single `.a` file.
- **List contents of a static library**: Inspect what object files are inside a `.a` file.
- **Extract object files**: Pull object files out of a static library for further analysis or modifications.

#### Key Commands:
- **Create a static library**:
  ```bash
  ar rcs libmylibrary.a file1.o file2.o
  ```
  - `r`: Replace or add object files to the archive.
  - `c`: Create the archive if it doesn’t exist.
  - `s`: Write an index to the archive for faster linking.

- **List contents of a static library**:
  ```bash
  ar -t libmylibrary.a
  ```
  This shows the names of all object files inside the library.

- **Extract object files from a library**:
  ```bash
  ar -x libmylibrary.a
  ```
  This extracts all `.o` files from the archive into the current directory.

---

### 2. **`nm` (Name List)**

`nm` is used to display the symbols (functions, variables, etc.) from object files, libraries, or executables. It helps developers inspect what symbols are defined or referenced in a binary file.

#### Common Use Cases:
- **Inspect symbols in a library or object file**: See which functions or variables are exported.
- **Debug missing symbols**: Identify which symbols are undefined in a library and which are provided.
- **Understand symbol visibility**: Check if a symbol is public, static, or undefined.

#### Key Commands:
- **List all symbols**:
  ```bash
  nm libmylibrary.a
  ```
  Outputs a list of symbols, their types, and memory addresses.

- **Filter undefined symbols**:
  ```bash
  nm libmylibrary.a | grep " U "
  ```
  This shows only undefined symbols (`U` stands for undefined).

- **Filter defined symbols**:
  ```bash
  nm libmylibrary.a | grep " T "
  ```
  This shows symbols defined in the text section (`T` stands for text, i.e., code).

#### Symbol Types in `nm`:
- `T`: Defined in the text (code) section.
- `D`: Defined in the data section.
- `B`: Defined in the BSS (uninitialized data) section.
- `U`: Undefined (needs to be resolved at link time).

---

### Practical Example:
Suppose you have a static library `libexample.a` and want to check its contents and symbols:

1. **List object files in the library**:
   ```bash
   ar -t libexample.a
   ```
   Output:
   ```
   file1.o
   file2.o
   ```

2. **Inspect symbols in the library**:
   ```bash
   nm libexample.a
   ```
   Output:
   ```
   file1.o:
   00000000 T function_in_file1
   U external_function

   file2.o:
   00000000 T function_in_file2
   00000000 D global_variable
   ```

   This shows that:
   - `function_in_file1` and `function_in_file2` are defined in the library.
   - `external_function` is undefined, meaning the linker must find it elsewhere.

---

### When to Use `ar` and `nm`:
- **`ar`**: Use it to manage static libraries, combine object files, or inspect their contents.
- **`nm`**: Use it to debug missing symbols, inspect symbol visibility, or analyze dependencies between libraries.

These tools are essential for low-level debugging and managing static libraries, especially in C and C++ projects.
