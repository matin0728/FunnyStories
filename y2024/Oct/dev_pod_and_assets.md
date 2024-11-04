# How can I create a assets bundle on a local dev cocoapods and access image from that? #

To create an asset bundle in a local CocoaPods development pod and access images from it in your iOS app, you can follow these steps:

### Step 1: Create an Asset Catalog in the Pod

1. In your development pod, create a new folder for assets (e.g., `Assets.xcassets`).
2. Inside this folder, create an asset catalog with your images:
   - Right-click in the Finder (or use Xcode) to create `Assets.xcassets`.
   - Inside `Assets.xcassets`, add image sets for your images (e.g., `MyImage.imageset`) and add your images to the set.

Your directory structure should look something like this:

```
YourPodName/
├── Assets.xcassets
│   └── MyImage.imageset
│       ├── my_image@1x.png
│       ├── my_image@2x.png
│       └── my_image@3x.png
└── YourPodName.podspec
```

### Step 2: Update the Podspec to Include the Asset Catalog

In your `YourPodName.podspec` file, you need to specify that the asset catalog should be included in the resources for the pod.

1. Open your podspec file (`YourPodName.podspec`).
2. Add the `resource_bundles` attribute to specify the asset catalog:

   ```ruby
   Pod::Spec.new do |s|
     s.name             = 'YourPodName'
     s.version          = '1.0.0'
     s.summary          = 'A summary of YourPodName.'
     s.description      = 'A description of YourPodName.'
     s.homepage         = 'https://example.com/YourPodName'
     s.license          = { :type => 'MIT', :file => 'LICENSE' }
     s.author           = { 'Author' => 'author@example.com' }
     s.source           = { :git => 'https://example.com/YourPodName.git', :tag => s.version.to_s }
     s.ios.deployment_target = '13.0'

     # Define source files and resource bundles
     s.source_files = 'YourPodName/**/*.{swift,h,m}'
     s.resource_bundles = {
       'YourPodNameAssets' => ['YourPodName/Assets.xcassets']
     }
   end
   ```

   Here, `YourPodNameAssets` is the name of the bundle that will be created for your assets.

### Step 3: Access the Image from the Bundle in Your Code

Once you've included the assets in your podspec, you can load images from the bundle in your app or pod code. In Swift, you can use the `Bundle` class to access the specific bundle created for your assets.

```swift
// Load an image from the bundle
let bundle = Bundle(for: YourClassInThePod.self) // Reference a class in the pod
let image = UIImage(named: "MyImage", in: bundle, compatibleWith: nil)
```

- Replace `YourClassInThePod.self` with any class from your pod to correctly locate the bundle.
- Use the exact name of your image set (e.g., `"MyImage"`) when loading the image.

### Step 4: Test the Pod in Your App

1. Ensure your app uses the development version of the pod by specifying it in your `Podfile`:

   ```ruby
   pod 'YourPodName', :path => '~/path/to/YourPodName'
   ```

2. Run `pod install` to update the pod in your project.
3. Build and run the app, and confirm that the image loads correctly.

This setup will allow you to bundle assets in a local CocoaPod, access them from code, and use them in your app during development.