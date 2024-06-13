[app]

# (str) Title of your application
title = santhushare

# (str) Package name
package.name = santhushare

# (str) Package domain (needed for android/ios packaging)
package.domain = org.files

# (str) Source code where the main.py live
source.include_exts = py,png,jpg,kv,atlas,ico
#source.include_patterns = assets/*,images/*.png

# (list) Application requirements
requirements = kivy, pillow, kivymd,python3

# (int) Target Android API, should be as high as possible.
# android.api = 27

# (int) Minimum API your APK will support.
android.api = 21

# (int) Android SDK version to use
android.sdk = 28

# (str) Android NDK version to use
android.ndk = 21.1.6352462

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path = /home/kivy/Android/Sdk/ndk/21.1.6352462

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path = /home/kivy/Android/Sdk

# (str) Python for android build path
android.p4a_dir = /root/.local/share/python-for-android

# (str) Path to build artifact storage, absolute or relative to spec file
# (this should be your current directory)
# The build directory is used to store cached object files and other temporary files
build_dir = .buildozer

# (int) Color depth (either 16, 24, or 32)
orientation = portrait

# (bool) Whether the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# android.permissions = INTERNET

# (list) Features (adds uses-feature -tags to manifest)
# android.features = android.hardware.camera

# (list) Application meta-data (key=value pairs)
# android.meta_data = key=value

# (list) Extra android activities to declare (here, added a PythonActivity)
android.add_activites = com.example.ExampleActivity:android:label:ExampleActivity

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (str) OUYA console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# android.ouya.category = GAME

# (str) Filename of icon (should be copied to /images/icon.png)
icon.filename = logo.ico
presplash.filename=logo.ico
# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
# orientation = portrait

# (bool) If True, then the screen will not turn off automatically
# wake_lock = False

# (list) Permissions
# permissions = INTERNET

# (list) Features (adds uses-feature -tags to manifest)
# android.features = android.hardware.usb.host

# (list) Application meta-data (key=value pairs)
# android.meta_data = key=value

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so

# (list) Android additional libraries to copy into libs/armeabi-v7a
# android.add_libs_armeabi_v7a = libs/android-v7/*.so

# (list) Android additional libraries to copy into libs/arm64-v8a
# android.add_libs_arm64_v8a = libs/android64/*.so

# (list) Android additional libraries to copy into libs/x86
# android.add_libs_x86 = libs/android-x86/*.so

# (list) Android additional libraries to copy into libs/x86_64
# android.add_libs_x86_64 = libs/android-x86_64/*.so

# (list) Android add-ons to use
# android.add_ons = pymunk

# (str) Android app theme, style name
# android.app_theme = @android:style/Theme.NoTitleBar

# (str) Launch mode for the activity
# android.activity_launch_mode = standard

# (list) Android intents to add to intent filters
# android.intents =



# (list) Python modules to compile
# python_modules = sqlite3,kivy

# (str) Python main entry point
entry_point = main.py

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir = 

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir = 

# (list) python-for-android whitelist
# p4a.whitelist = 

# (str) OUYA console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# android.ouya.category = GAME

# (bool) If True, then the screen will not turn off automatically
# wake_lock = False

# (list) Android permissions
# android.permissions = INTERNET

# (str) Backend to use, one of (pygame, sdl2, other)
#osx.python_version = 3
#ios.kivy_version = 1.11.1
#ios.codesign.identity = iPhone Developer

# (list) Permissions
# android.permissions = INTERNET

# (list) Features (adds uses-feature -tags to manifest)
# android.features = android.hardware.usb.host

# (list) Application meta-data (key=value pairs)
# android.meta_data = key=value

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so

# (list) Android additional libraries to copy into libs/armeabi-v7a
# android.add_libs_armeabi_v7a = libs/android-v7/*.so

# (list) Android additional libraries to copy into libs/arm64-v8a
# android.add_libs_arm64_v8a = libs/android64/*.so

# (list) Android additional libraries to copy into libs/x86
# android.add_libs_x86 = libs/android-x86/*.so

# (list) Android additional libraries to copy into libs/x86_64
# android.add_libs_x86_64 = libs/android-x86_64/*.so

# (list) Android add-ons to use
# android.add_ons = pymunk

# (str) Android app theme, style name
# android.app_theme = @android:style/Theme.NoTitleBar

# (str) Launch mode for the activity
# android.activity_launch_mode = standard

# (list) Android intents to add to intent filters
# android.intents =


# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D
