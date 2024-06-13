[app]

title = santhushare
package.name = testapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ico
presplash.filename = logo.ico

# (str) Icon of the application
icon.filename = logo.ico
version = 0.1
requirements = python3,kivy,kivymd,pillow
source.main = main.py  # Specify your entry point here
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
