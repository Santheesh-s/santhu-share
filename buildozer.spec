[app]

# (str) Title of your application
title = YourAppName

# (str) Package name
package.name = yourappname

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yourdomain

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (e.g. python files, kivy files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (backups, generated files, ...)
#source.exclude_exts = spec

# (list) List of inclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (int) Application versioning (method 2)
#version.regex = __version__ = ['"](.*)['"]
#version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (list) Application services
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (str) Android SDK version to use
#android.sdk = 20

# (int) Android minimum API version to use
android.api = 21

# (int) Android API version to use
#android.minapi = 21

# (int) Android API version to use
android.minapi = 21

# (int) Android API version to use
android.targetapi = 29

# (bool) Use the SD card as storage
#android.sdcard = False

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = False

# (str) Logcat filters for debugging
#android.logcat_filters = *:S python:D

# (bool) Use --private data storage
#android.private_storage = True

# (str) Android NDK version to use
#android.ndk = 17c

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
#android.apptheme = '@android:style/Theme.NoTitleBar'

# (list) Pattern to whitelist for the whole project
#p4a.whitelist =

# (str) Path to a custom whitelist file
#p4a.whitelist_src =

# (str) Path to a custom blacklist file
#p4a.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards.
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
#android.add_aars =

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# bootstrap)
#android.gradle_dependencies = 'com.android.support:support-v4:24.1.1'

# (list) packaging options to add (currently works only with sdl2_gradle
# bootstrap)
#android.packaging_options =

# (list) Java classes to add to the android project (can be .java or .class files)
#android.add_classpath = com/dropbox/core/Dropbox.class

# (str) subclass of org.kivy.android.PythonActivity
#android.activity_theme = 

# (str) Android app theme, default is okay for Kivy-based app
# This setting can be overriden in the `buildozer.spec` file
# android.apptheme = 

# (bool) Android Java debugger
#android.debug = False

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a = libs/android-v7/*.so

# (list) Android additional libraries to copy into libs/arm64-v8a
#android.add_libs_arm64_v8a = libs/android-v8/*.so

# (list) Android additional libraries to copy into
