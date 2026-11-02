[app]
title = Prorab Smeta
package.name = prorabsmeta
package.domain = org.abdulla

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

# Talab qilinadigan kutubxonalar (ReportLab va Pillow PDF uchun kerak)
requirements = python3,kivy,reportlab,pillow

# Android 10+ (API 29+) talablari
android.api = 33
android.minapi = 29
android.ndk = 25b

# Xotiraga kirish ruxsatlari
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Android 10+ xotira cheklovini yengish uchun:
android.manifest.requestLegacyExternalStorage = True

orientation = portrait
fullscreen = 0