# Compile curl from source #

> How to add SSL support when I compile the lib "curl" from source?

To add SSL support when compiling `libcurl` from source, you need to make sure that `libcurl` can find and link against an SSL library. The most common SSL libraries used with `libcurl` are OpenSSL, LibreSSL, or mbedTLS. Below are the steps to compile `libcurl` with SSL support using OpenSSL as an example:

### Step 1: Install Dependencies

Make sure you have the required build tools and SSL libraries installed. You can install OpenSSL using a package manager. For example:

- **On Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install build-essential libssl-dev
  ```

- **On CentOS/RHEL**:
  ```bash
  sudo yum groupinstall "Development Tools"
  sudo yum install openssl-devel
  ```

- **On macOS** (use Homebrew):
  ```bash
  brew install openssl
  ```

### Step 2: Download `libcurl` Source Code

You can download the latest version of `libcurl` from the official website:

```bash
curl -O https://curl.se/download/curl-8.4.0.tar.gz
tar -xzf curl-8.4.0.tar.gz
cd curl-8.4.0
```

### Step 3: Configure the Build

When configuring the build, specify that you want to use OpenSSL. You might also need to provide the path to the OpenSSL installation if it’s not in a standard location.

- **On Linux**:
  ```bash
  ./configure --with-ssl --prefix=/usr/local
  ```

- **On macOS** (since OpenSSL may not be in the standard system paths):
  ```bash
  ./configure --with-ssl=/usr/local/opt/openssl --prefix=/usr/local
  ```

**Note**: Adjust the `--with-ssl` path if your OpenSSL is installed elsewhere.

### Step 4: Compile and Install

Run the following commands to build and install `libcurl`:

```bash
make
sudo make install
```

### Step 5: Verify SSL Support

To ensure that `libcurl` was built with SSL support, you can check it using:

```bash
curl --version
```

You should see something like this in the output:
```
curl 8.4.0 (x86_64-pc-linux-gnu) libcurl/8.4.0 OpenSSL/1.1.1l
Protocols: dict file ftp ftps http https ...
Features: AsynchDNS IPv6 Largefile SSL
```

The presence of `OpenSSL` and `https` indicates that SSL support is enabled.

### Step 6: (Optional) Set Library Path

If you installed `libcurl` in a custom directory (e.g., `/usr/local`), you might need to add the library path to your system’s library path:

- **On Linux**:
  ```bash
  export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  ```

- **On macOS**:
  ```bash
  export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH
  ```

You can add this line to your `.bashrc` or `.bash_profile` to make the change persistent.

### Troubleshooting

1. **Missing SSL Libraries**:
   If `configure` reports that it can't find OpenSSL, ensure that the `libssl-dev` (or `openssl-devel`) package is installed, and verify the path you provide in the `--with-ssl` option.

2. **Compile Errors**:
   If there are errors related to OpenSSL during compilation, ensure that your OpenSSL version is compatible with `libcurl`. Consider updating OpenSSL if it’s outdated.

By following these steps, you should be able to compile `libcurl` with SSL support enabled.