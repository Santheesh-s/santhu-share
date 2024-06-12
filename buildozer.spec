[app]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myapp

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ico

# (list) Application dependencies
requirements = python3, kivy, kivymd ,pillow

# (str) Presplash of the application
presplash.filename = assets/images/logo.ico

# (str) Icon of the application
icon.filename = assets/images/logo.ico

# (str) Supported orientation (one of: landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (list) Features (adds uses-feature -tags to manifest)
android.features = android.hardware.camera, android.hardware.camera.autofocus

# (str) The Android entry point. You should not need to change this.
android.entrypoint = org.kivy.android.PythonActivity

# (str) The directory in which python is unpacked
android.unpacked_libs = libs

# (str) Android API to use
android.api = 31

# (str) Minimum API allowed for Android
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) If true, enables AndroidX support. (used in recent Android SDKs)
android.enable_androidx = True

# (list) Patterns to exclude from the build
# (example: exclude all .txt files)
exclude_patterns = license,images/*.tmp

# (list) List of Java .jar files to add to the libs dir
#android.add_jars = myJar.jar
