def hashing(siteName):
    hashSite = 0
    site = siteName[siteName.find('.')+1:]
    site = site[:site.find('.')]
    site = site.upper()
    for i in range(len(site)):
        print(site[i])
        hashSite += ord(site[i])
    return hashSite
print(hashing('www.google.com'))
