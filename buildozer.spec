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

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.1.0,kivymd==0.104.2,pillow==8.3.1

# (str) Presplash of the application
presplash.filename = %(source.dir)s/"logo for SANTHU SHARE.ico"

# (str) Icon of the application
icon.filename = %(source.dir)s/"logo for SANTHU SHARE.ico"

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# Android specific settings
[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash background color (for android toolchain)
android.presplash_color = black

# (bool) Allow backup for the application
android.allow_backup = True
