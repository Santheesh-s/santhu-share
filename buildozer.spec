[app]
# (str) Title of your application
title = Santhu Share
source.dir=.
# (str) Package name
package.name = santhusshare
orientation = portrait
# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py is located
source.include_exts = py,png,jpg,kv,atlas,ico

# (str) Application versioning (MAJOR.MINOR.PATCH)
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE


# (list) Features (added as a list of features)
# (str) Presplash of the application
presplash.filename = logo.ico
icon.filename=logo.ico
