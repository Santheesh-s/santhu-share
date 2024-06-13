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
# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, CAMERA

# (int) Target Android API, should be as high as possible.
android.api = 29

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Icon of the application

# (str) Path to images directory
# presplash_path = %(source.dir)s/presplash.png

# (str) Path to icon directory
# icon_path = %(source.dir)s/icon

# (str) Android App use python-for-android
# p4a.source_dir = /home/kivy/Desktop/kivy/examples/demo/touchtracer

# (str) Python-for-android git branch (defaults to master)
# p4a.branch = develop

# (str) Python-for-android git commit (defaults to HEAD)
# p4a.revision = HEAD
# Application requirements (comma-separated)
requirements = python3,kivy,kivymd,pillow

# Minimum API needed
osx.python_version = 3

# Permissions
#android.permissions = INTERNET

# Android-specific settings

# Target Android API

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
