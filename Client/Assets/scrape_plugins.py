#!/usr/local/bin/python

from lxml import html
import os
import requests
import shutil
import urllib

def main():
    if not os.path.exists("SearchPlugins"):
        os.makedirs("SearchPlugins")

    locales = getLocaleList()
    for locale in locales:
        files = getFileList(locale)
        if files is None:
            continue

        print("found searchplugins")

        for file in files:
            downloadedFile = getFile(locale, file)
            directory = os.path.join("SearchPlugins", locale)
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.move(downloadedFile, os.path.join(directory, file))

def getLocaleList():
    response = requests.get('http://hg.mozilla.org/releases/mozilla-aurora/raw-file/default/mobile/android/locales/all-locales')
    return response.text.strip().split("\n")

def getFileList(locale):
    print("scraping: {0!s}...".format(locale))
    url = "https://hg.mozilla.org/releases/l10n/mozilla-aurora/{0!s}/file/default/mobile/searchplugins".format(locale)
    response = requests.get(url)
    if not response.ok:
        return

    tree = html.fromstring(response.content)
    return tree.xpath('//a[@class="list"]/text()')

def getFile(locale, file):
    print("  downloading: {0!s}...".format(file))
    url = "https://hg.mozilla.org/releases/l10n/mozilla-aurora/{0!s}/raw-file/default/mobile/searchplugins/{1!s}".format(locale, file)
    result = urllib.urlretrieve(url)
    return result[0]

if __name__ == "__main__":
        main()

