[app]

# Title of your application
title = santhushare

# Package name
package.name = files

# Package domain
package.domain = org.santhushare

# Source code directory
source.dir = .

# Source files to include
source.include_exts = ico,py,png,jpg,kv,txt,atlas

# List of inclusions using pattern matching
source.include_patterns = images/*.png

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy==2.1.0,kivymd==0.104.2,pillow==8.3.1

# Presplash of the application
presplash.filename = %(source.dir)s/"logo for SANTHU SHARE.ico"

# Icon of the application
icon.filename = %(source.dir)s/"logo for SANTHU SHARE.ico"

# Supported orientation
orientation = portrait

[buildozer]

# Log level
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# Path to build output storage
bin_dir = ./bin

# Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a
