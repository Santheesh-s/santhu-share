[app]

# (str) Title of your application
title = YourAppTitle

# (str) Package name
package.name = yourapppackage

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py file is located
source.dir = .

# (str) The version of your application, keep it in a format x.y.z
version = 0.1

# (str) Icon of the application
icon.filename = icon.png

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = kivy,python3crystax

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
# Default is 27.
android.api = 29

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 28

# (int) Android NDK version to use
android.ndk = 21.1.6352462

# (bool) Use the --private data flag
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_path = /path/to/your/ndk

# (bool) Use the CrystaX NDK
android.ndk_cython = False

# (bool) Use Cython for JNI parts
android.arch = armeabi-v7a

# (list) Android additionnal libraries to copy into libs/armeabi
android.add_libs_armeabi = /path/to/your/libs

# (list) Android additionnal libraries to copy into libs/arm64-v8a
android.add_libs_arm64_v8a = /path/to/your/libs

# (list) Android additionnal libraries to copy into libs/x86
android.add_libs_x86 = /path/to/your/libs

# (list) Android additionnal libraries to copy into libs/x86_64
android.add_libs_x86_64 = /path/to/your/libs

# (list) Android additionnal Java files to copy into src
#android.add_src = jni/foo.java

# (list) Android Application remove permissions, comma separated
#android.permissions.remove = INTERNET

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA category will not be added
android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters = filters.xml

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional metadata elements to include in the manifest
#android.manifest.meta_data = com.example.meta_data_key=my Metadata

# (list) Android additional uses-library elements to include in the manifest
#android.manifest.uses_library = com.google.android.maps

# (list) Android additional uses-permission elements to include in the manifest
#android.manifest.uses_permission = com.example.permission

# (str) Android XML file to parse (can use more than one for different parts)
#android.manifest.extra_xml = 

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.arch = armeabi-v7a

# (str) The name of the OUYA developer key
#android.ouya.developer_key = key

# (str) python-for-android branch to use, defaults to master
#p4a.branch = develop

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = my_recipes

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (str) directory containing recipe for python3crystax that should be used
#p4a.python3crystax = /home/kivy/venvcrystax

# (list) Application source code
# You can add your own python file or list of files here
#source.include_exts = py,png,jpg,kv,atlas,json
#source.include_patterns = assets/*,images/*.png
#source.exclude_patterns = license.txt,data/audio/*.wav
#source.exclude_exts = spec

# (str) Custom source folders for inclusion
#source.custom_exts = myext.py:app

# (str) The directory where the cache of the cacheable dependencies are
#p4a.local_build_cache = ./.buildozer/android/platform/build-armeabi-v7a

# (list) Include sqlite3.so
#p4a.include_sqlite3 = 1

# (list) Include openssl
#p4a.include_openssl = 1

# (list) Include python modules as zip file
#p4a.presplash.ziproot = /path/to/zip/file

# (list) Include precompiled python modules
#p4a.presplash.precompiled = pygame

# (list) Include precompiled python modules as zip file
#p4a.python_modules = requests, json

# (str) URL of python distribution to use, if empty defaults to
# https://python.org/ftp/python/ + version
#p4a.python_branch = 3.8

# (str) The name of the python-for-android dist default is "default"
#p4a.dist_name = mydist

# (str) The bootstraps to build for android separated by comma
#p4a.bootstraps = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# (str) Python build recipe to use for python build
# p4a.recipe = 

# (str) Directory to copy application specific data files
#p4a.datas = 

# (str) Directory to copy python dependencies (for sqlite3 SSL support)
#p4a.depends = 

# (str) Extra arguments for android compilation phase
#p4a.extra_args = --link-classes=jni -L/path/to/lib/

# (str) Extra arguments for android build phase
#p4a.build_args = -j 4

# (str) Path to a custom Java bootstrap to include instead of default
#p4a.javahost_bootstrap = /path/to/javahost/bootstrap.jar

# (str) bootstrap to use for android builds (deprecated)
# p4a.bootstrap = sdl2

# (str) version of crystax ndk to use
# p4a.crystax = 10.3.2

# (str) Android entry point
#p4a.entry_point = org.kivy.android.PythonActivity

# (list) Application source code (python files)
#source.include_exts = py,png,jpg,kv,atlas,json
#source.include_patterns = assets/*,images/*.png
#source.exclude_patterns = license.txt,data/audio/*.wav
#source.exclude_exts = spec

# (str) package name
#package.name = myapp

# (str) Android entry point
#p4a.entry_point = org.kivy.android.PythonActivity

# (str) Android app theme, default is '@android:style/Theme.NoTitleBar'
# https://developer.android.com/guide/topics/ui/look-and-feel/themes
#android.theme = '@android:style/Theme.NoTitleBar'

# (bool) Enable Android Java debugging
#p4a.java_debug = False

# (str) NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = 

# (str) bootstrap to use for android builds (deprecated)
#p4a.bootstrap = sdl2

# (str) Android app theme, default is '@android:style/Theme.NoTitleBar'
# https://developer.android.com/guide/topics/ui/look-and-feel/themes
#android.theme = '@android:style/Theme.NoTitleBar'

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (bool) Uses (and includes) crystax NDK
#p4a.crystax = 1
