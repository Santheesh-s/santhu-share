[app]

# Title of your application
title = SANTHU'S SHARE

# Package name
package.name = santhushare

# Package domain (needed for android/ios packaging)
package.domain = org.files

# Source code directory
source.dir = .

# Output directory for the package
build.dir = .

# Application version
version = 0.1

# Supported orientation
orientation = portrait

# Application requirements (comma-separated)
requirements = python3,kivy=2.0.0,pillow

# Minimum API needed
osx.python_version = 3

# Permissions
#android.permissions = INTERNET

# Android-specific settings
[app]

# Target Android API
android.api = 29

# Android SDK version to use
android.sdk = 20

# Android NDK version to use
android.ndk = 19b

# Android NDK API to use (minimum API supported)
android.ndk_api = 21

# Application icon file
icon.filename = %(source.dir)/logo.ico

# Splash screen (pre-splash) image file
presplash.filename = %(source.dir)/logo.ico
# Android architecture to build for (armeabi-v7a by default)
#android.arch = armeabi-v7a

# Android entry point (default is okay for Kivy-based app)
#android.entrypoint = org.kivy.android.PythonActivity

# Android app theme (default is okay for Kivy-based app)
#android.apptheme = "@android:style/Theme.NoTitleBar"

# iOS specific settings (optional)
#[app]

# Path to a custom kivy-ios folder (if using Kivy for iOS)
#ios.kivy_ios_dir = ../kivy-ios

# iOS SDK version to use
#ios.sdk = 12.1

# iOS Python interpreter version (2 by default)
#ios.python_version = 2

# iOS bundle identifier
#ios.bundle_identifier = com.example.myapp

# Enable on-demand resources for the game (True/False)
#ios.on_demand_resources = False

# The iCloud container to use for the app
#ios.icloud_container = com.example.myapp

# The iCloud document versioning identifier
#ios.icloud_document_versioning = ''

# Entitlements file for the app
#ios.entitlements = ''

# Application bundle to use for the app
#ios.app_bundle = ''

# Launch storyboard file of the app
#ios.launch_storyboard = ''

# URL scheme to use for the app
#ios.url_scheme = myapp
