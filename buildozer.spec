[app]

# (str) Title of your application
title = YourAppName

# (str) Package name
package.name = com.santhu

# (str) Package domain (needed for android/ios packaging)
package.domain = org.santhushare

# (str) Source code where the main.py live
source.dir = .

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = kivy, requests, kivymd,pillow

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

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
icon.filename = logo.ico

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
