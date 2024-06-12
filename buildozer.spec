[app]
# (str) Title of your application
title = Santhushare

# (str) Package name
package.name = santhushare

# (str) Package domain (needed for android/ios packaging)
package.domain = org.santhushare

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd,cython,pillow,requests,chardet,idna,urllib3,certifi,wikipedia,soupsieve,beautifulsoup4

# (str) Presplash of the application
presplash.filename = %(source.dir)s/logo.ico

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.ico

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android API to use
android.api = 31

# (str) Minimum Android API to support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 21b

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Build output directory
bin_dir = ./bin

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
