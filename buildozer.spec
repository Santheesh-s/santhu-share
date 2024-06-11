[app]

# (str) Title of your application
title = SanthusShare

# (str) Package name
package.name = santhussahre

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (str) Source files to include (e.g. python files, kivy files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of application requirements
requirements = python3,kivy

# (int) Android API version to use
android.api = 21

# (int) Android minimum API version to use
android.minapi = 21

# (int) Android target API version
android.targetapi = 29

# (list) Android architectures to build for
android.archs = armeabi-v7a

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = False

# (list) Permissions
android.permissions = INTERNET

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = /path/to/android/sdk

# (str) Path to the Android build tools directory
android.build_tools = /path/to/android/sdk/build-tools/xx.x.x

# (str) Path to the Android SDK tools directory
android.sdk_tools = /path/to/android/sdk/tools

# (str) Application versioning (method 1)
version = 1.0

# (list) Application author
author = Your Name

# (str) Application description
description = Your application description

# (str) Application icon (place icon.png in the images directory)
icon.filename = images/icon.png

# (list) Permissions
android.permissions = INTERNET
