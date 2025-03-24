# How to create config for static lib

> I have a lib written in C++, by default I run "cmake" and "make", it gave me several executables,
> but what I want is compile it to a static lib which can be used in an iOS app, how can I do that?

To compile your C++ library into a static library for use in an iOS app, you can adjust your `CMakeLists.txt` to produce a static library instead of executables. Here’s a step-by-step guide:

---

### 1. Modify `CMakeLists.txt`

Change the target type in your `CMakeLists.txt` to generate a static library:

- Locate the section where the targets are defined.
- Replace `add_executable()` with `add_library()` for your library target.

For example:

```cmake
# Replace this
add_executable(my_executable source1.cpp source2.cpp)

# With this
add_library(my_library STATIC source1.cpp source2.cpp)
```

---

### 2. Set Target Platform to iOS

Add the necessary settings for iOS in your `CMakeLists.txt`. iOS static libraries must be built for specific architectures (e.g., `arm64` for devices, `x86_64` for the simulator). Here’s an example configuration:

```cmake
# Specify the minimum iOS version
set(CMAKE_OSX_DEPLOYMENT_TARGET "12.0")

# Specify iOS as the platform
set(CMAKE_SYSTEM_NAME iOS)

# Specify the architectures to build for
set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64")
```

---

### 3. Build the Static Library

Run the following commands to build the library:

```bash
mkdir build && cd build
cmake -DCMAKE_TOOLCHAIN_FILE=<path_to_ios_toolchain> -G "Unix Makefiles" ..
make
```

- Replace `<path_to_ios_toolchain>` with a toolchain file like [iOS.toolchain.cmake](https://github.com/leetal/ios-cmake) or your own custom toolchain.
- The output will be a `.a` file (static library).

---

### 4. Combine Architectures into a Universal Static Library

After building for device (`arm64`) and simulator (`x86_64`), you need to combine the libraries into a universal library using `lipo` or `libtool`.

For example:

```bash
lipo -create -output libMyLibrary.a build-arm64/libMyLibrary.a build-x86_64/libMyLibrary.a
```

---

### 5. Link the Static Library in Your iOS App

Add the generated `.a` file to your iOS app's Xcode project:

1. Drag the `.a` file into your Xcode project.
2. Ensure the `.a` file is included in the "Link Binary with Libraries" section of your target's build phases.
3. Add any dependent headers or paths to your project settings under **Header Search Paths**.

---

### 6. Test the Integration

Make sure your library functions as expected by calling its methods from your iOS app. If you encounter issues, verify the architecture compatibility between the library and your app.

Let me know if you need help with any specific step!
