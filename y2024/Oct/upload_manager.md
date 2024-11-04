# Upload Manager #

```
Write a C++ class called UploadManager, has a "upload" method and callback, using "curl" send a post request with headers and parameters, the parameter is an array of "event" struct and send with json serialized data, the "event" object has following fields: "id" which is string, "quantity" which is a int, and the response is json format: {"message": "some message", "request_id": "some id", "results": [{"id": string, "code": "some code", "message": "some message"}, ...]}, you need check the HTTP status, if the request is successful, parse the response and map every entry in "results" field to another object with fileds: id and code, and call the callback function with the mapped array.
```

Here’s a C++ implementation of the `UploadManager` class using `libcurl` to send a POST request with headers and parameters. The request sends serialized JSON data of `event` structs, and upon receiving the response, it checks the HTTP status and maps the `results` field from the JSON response to another object with `id` and `code`. The callback function is invoked with this mapped data.

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <functional>
#include <curl/curl.h>
#include <json/json.h>

// Event struct
struct Event {
    std::string id;
    int quantity;
};

// Result struct
struct Result {
    std::string id;
    std::string code;
};

// UploadManager class
class UploadManager {
public:
    using Callback = std::function<void(const std::vector<Result>&)>;

    // Constructor
    UploadManager() {
        curl_global_init(CURL_GLOBAL_DEFAULT);
    }

    // Destructor
    ~UploadManager() {
        curl_global_cleanup();
    }

    // Method to upload events
    void upload(const std::vector<Event>& events, Callback callback) {
        CURL* curl = curl_easy_init();
        if (!curl) {
            std::cerr << "Failed to initialize CURL" << std::endl;
            return;
        }

        // Set up URL and headers
        std::string url = "https://example.com/upload";
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        // Serialize events to JSON
        std::string jsonData = serializeEvents(events);

        // Set CURL options
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());

        // Response handling
        std::string responseString;
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

        // Perform the request
        CURLcode res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK) {
            std::cerr << "CURL request failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            long httpCode = 0;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
            if (httpCode == 200) {
                std::vector<Result> results = parseResponse(responseString);
                callback(results);
            } else {
                std::cerr << "HTTP error: " << httpCode << std::endl;
            }
        }

        // Cleanup
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }

private:
    // Method to serialize events to JSON
    std::string serializeEvents(const std::vector<Event>& events) {
        Json::Value root;
        for (const auto& event : events) {
            Json::Value eventJson;
            eventJson["id"] = event.id;
            eventJson["quantity"] = event.quantity;
            root.append(eventJson);
        }

        Json::StreamWriterBuilder writer;
        return Json::writeString(writer, root);
    }

    // Method to parse JSON response
    std::vector<Result> parseResponse(const std::string& response) {
        std::vector<Result> results;
        Json::CharReaderBuilder reader;
        Json::Value root;
        std::string errs;

        std::istringstream sstr(response);
        if (Json::parseFromStream(reader, sstr, &root, &errs)) {
            const Json::Value resultsJson = root["results"];
            for (const auto& resultJson : resultsJson) {
                Result result;
                result.id = resultJson["id"].asString();
                result.code = resultJson["code"].asString();
                results.push_back(result);
            }
        } else {
            std::cerr << "Failed to parse JSON response: " << errs << std::endl;
        }
        return results;
    }

    // CURL write callback
    static size_t writeCallback(void* contents, size_t size, size_t nmemb, std::string* userData) {
        size_t totalSize = size * nmemb;
        userData->append((char*)contents, totalSize);
        return totalSize;
    }
};

int main() {
    // Example usage of UploadManager
    UploadManager uploadManager;

    // Create sample events
    std::vector<Event> events = {
        {"event1", 10},
        {"event2", 5}
    };

    // Define callback to handle the response
    auto callback = [](const std::vector<Result>& results) {
        for (const auto& result : results) {
            std::cout << "ID: " << result.id << ", Code: " << result.code << std::endl;
        }
    };

    // Perform the upload
    uploadManager.upload(events, callback);

    return 0;
}
```

### Breakdown:

1. **UploadManager class:**
   - Contains the `upload` method, which sends a POST request using `libcurl`.
   - Accepts a list of `Event` objects and a callback function as parameters.

2. **Events serialization:**
   - The `serializeEvents` method converts the `Event` objects into a JSON array.

3. **CURL setup:**
   - Sets headers (`Content-Type: application/json`), URL, and serialized JSON data as the POST body.
   - Handles the response via the `writeCallback` function.

4. **Response parsing:**
   - If the HTTP status is 200, the `parseResponse` method extracts the `results` array from the response and maps each entry to a `Result` object.

5. **Callback invocation:**
   - The callback function is invoked with the list of parsed `Result` objects.

Let me know if you'd like any further adjustments!