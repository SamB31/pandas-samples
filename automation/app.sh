#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Patriot Data Processing.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Patriot Data Processing.dmg" && rm "dist/Patriot Data Processing.dmg"
create-dmg \
  --volname "Patriot Data Processing" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --app-drop-link 425 120 \
  "dist/Patriot Data Processing.dmg" \
  "dist/dmg/"