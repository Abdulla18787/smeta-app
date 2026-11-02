[app]
title = Prorab Smeta
package.name = prorabsmeta
package.domain = org.abdulla

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy,fpdf2

android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.manifest.requestLegacyExternalStorage = True

orientation = portrait
fullscreen = 0
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
