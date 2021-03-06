#!/usr/local/bin/python

import os
import requests

def main():
    locales = os.listdir("SearchPlugins")
    for locale in locales:
        default = getDefault(locale)
        if default is not None:
            saveDefault(locale, default)

def getDefault(locale):
    print("scraping: {0!s}...".format(locale))
    url = "https://hg.mozilla.org/releases/l10n/mozilla-aurora/{0!s}/raw-file/default/mobile/chrome/region.properties".format(locale)
    response = requests.get(url)
    if not response.ok:
        return

    lines = response.text.strip().split("\n")
    for line in lines:
        values = line.strip().split("=")
        if len(values) == 2 and values[0].strip() == "browser.search.defaultenginename":
            default = values[1].strip()
            print("  default:  {0!s}".format(default))
            return default

def saveDefault(locale, default):
    directory = os.path.join("SearchPlugins", locale, "default.txt")
    file = open(directory, "w")
    file.write(default.encode("UTF-8"))

if __name__ == "__main__":
        main()
