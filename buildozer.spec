[app]
# (str) Title of your application
title = Santhu Share

# (str) Package name
package.name = tkinterfileupload

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourdomain

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ico

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,data/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (str) Application versioning (method 1)
version = 0.1

# (str) Application identifier (method 2)
package.id = org.yourdomain.yourapp

# (list) Application dependencies
requirements = python3,kivy,kivymd,android

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (str) Path to the icon
icon.filename = logo.ico

# (str) Path to the splash screen
presplash.filename = logo.ico

# (str) Presplash background color (default is white)
presplash.background = #FFFFFF

# (list) Patterns to include from the build directory
source.include_patterns = assets/*,data/*

# (list) List of patterns to exclude from the build directory
source.exclude_patterns = tests/*,venv/*

# (str) Android entry point, default is main.py
android.entrypoint = main.py

# (str) Full name including first and last name
author.name = santheesh

# (str) Your email address
author.email = santheesh24@gmail.com

# (str) License
license = MIT

# (str) Supported architectures
android.archs = armeabi-v7a, arm64-v8a, x86, x86_64

# (str) Additional Java repositories
android.p4a_whitelist_repositories = 

# (str) Gradle dependency
#android.gradle_dependencies = 

# (list) Gradle repositories to search for dependencies
android.add_jars =

# (str) Additional jars
#android.add_aars =

# (str) Custom source files
android.add_src = 

# (list) Exclude files
android.exclude_patterns = 

# (list) Include files
android.include_patterns = 

# (list) Additional assets to be copied
android.add_assets = 

# (str) Additional source dirs
android.add_source =

# (list) List of gradle libraries
android.gradle_libraries =

# (str) Application data to include
android.include_data = 

# (str) File to use for versioning
android.release_artifacts = 

# (list) Excluded assets
android.exclude_assets = 

# (list) Include assets
android.include_assets = 

# (list) List of Android extra files
android.extra_files = 

# (list) Android other packaging options
android.other_packages =

# (list) Extra Android packaging options
android.extra_packaging = 

# (list) Files to be added to the release
android.release_additions = 

# (list) Custom assets directories
android.assets_directories = 

# (list) List of additional python packages
android.additional_python_packages = 

# (list) List of additional requirements
android.additional_requirements = 

# (list) Additional p4a arguments
android.p4a_arguments = 

# (str) Arguments to be passed to the SDK manager
android.sdk_args = 

# (str) Arguments to be passed to the ADB
android.adb_args = 

# (str) Path to a custom AndroidManifest.xml file
android.manifest = 

# (str) Path to the buildozer log file
log.filename = ./buildozer.log

# (str) Path to the buildozer version file
version.filename = ./buildozer.version

# (str) Path to the output directory
output.filename = ./bin

# (str) Path to the build directory
build.filename = ./build

# (list) List of strings with project requirements
requirements.spec =