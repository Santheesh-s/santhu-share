[app]

# Title of your applicatio
title = santhushare

# Package name
package.name = files

# Package domain (needed for Android/iOS packaging)
package.domain = org.santhushare

# Source code directory
source.dir = .

# Source files to include (let empty to include all the files)
source.include_exts = ico,py,png,jpg,kv,txt,atlas

# List of inclusions using pattern matching
source.include_patterns = images/*.png

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy==2.1.0,kivymd==0.104.2,pillow==8.3.1,requests,chardet,idna,urllib3,certifi,wikipedia,soupsieve,beautifulsoup4

# Presplash of the application
presplash.filename = %(source.dir)s/logo_for_SANTHU_SHARE.ico

# Icon of the application
icon.filename = %(source.dir)s/logo_for_SANTHU_SHARE.ico

# Supported orientation
orientation = portrait

# Permissions
android.permissions = INTERNET

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# Path to build output storage
bin_dir = ./bin

# Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# Android NDK version to use
android.ndk = 21.4.7075529

# Android API to use
android.api = 31

# Minimum Android API to support
android.minapi = 21
