[app]

# (str) Title of your application
title = santhushare

# (str) Package name
package.name = file

# (str) Package domain (needed for android/ios packaging)
package.domain = org.santhushare

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = ico,py,png,jpg,kv,txt,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = images/*.png

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.1.0,kivymd==0.104.2,pillow==8.3.1,requests,chardet,idna,urllib3,certifi,wikipedia,soupsieve,beautifulsoup4

# (str) Presplash of the application
presplash.filename = %(source.dir)s/logo.ico

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.ico

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build output storage
bin_dir = ./bin

# (list) Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Android NDK version to use
android.ndk = 21.4.7075529

# (str) Android API to use
android.api = 31

# (str) Minimum Android API to support
android.minapi = 21

# (str) Android SDK directory (if you are using a custom SDK)
android.sdk_path = /usr/local/lib/android/sdk

# (str) Android NDK directory (if you are using a custom NDK)
android.ndk_path = /usr/local/lib/android/sdk/ndk/21.4.7075529

# (str) Directory to store temporary build files
build_dir = .buildozer
