# Specify a single target to compile #

> I found I have multiple target, and the one I want is "marian", I use the command "cmake --build .",
> is that mean to compile all targets? How to compile only one target?

When you run `cmake --build .` without specifying a target, CMake builds **all the targets** in your project. If you want to build only a specific target, you can use the `--target` option to specify which target to build.

---

### How to Build a Specific Target

1. **Identify the Target Name:**
   - You already know the target name you want is `marian`. If you're unsure about the available targets, you can run:
     ```bash
     cmake --build . --target help
     ```
     This will list all the available targets in your project.

2. **Build Only the `marian` Target:**
   - Use the `--target` option to specify the target:
     ```bash
     cmake --build . --target marian
     ```

3. **Build with a Specific Configuration (if applicable):**
   - If you are building with a multi-config generator like Xcode or Visual Studio (e.g., `-G "Xcode"`), you must also specify the build configuration (e.g., Debug, Release):
     ```bash
     cmake --build . --target marian --config Release
     ```

4. **Specify Verbosity (Optional):**
   - To see detailed output during the build, you can add the `VERBOSE=1` option:
     ```bash
     cmake --build . --target marian -- VERBOSE=1
     ```

---

### Example with Full Command
If you're using the iOS toolchain and building only the `marian` target, your full command might look like this:
```bash
cmake --build . --target marian --config Release
```

---

### Notes
- If you only want to configure and build one target without including others in the build system, you can restructure your `CMakeLists.txt` to include only the necessary target and exclude others (not recommended for large projects with interdependencies).
- The `--target` option is helpful for selective builds, especially in projects with many targets or submodules.
