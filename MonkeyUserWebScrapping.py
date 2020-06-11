import requests, bs4, re, os

os.makedirs('monkeyUser', exist_ok=True)

invalidCharacters = '[!/?.*><|:@#$%\";]'
baseURL = 'https://www.monkeyuser.com'

currentURL = 'https://www.monkeyuser.com/2016/project-lifecycle/?dir=first'
comicIndex = 1
isLastComic = False
while not isLastComic:

    webRequest = requests.get(currentURL)
    webRequest.raise_for_status()
    webParsed = bs4.BeautifulSoup(webRequest.content, 'html.parser')

    nextLink = webParsed.select('div[class="thumb next nobefore"] a')
    isLastComic = len(nextLink) <= 0
    currentURL = baseURL + nextLink[0].get('href') if not isLastComic else currentURL

    imageLink = webParsed.select('div[class="content"] img')
    if len(imageLink) > 0:
        imageURL = imageLink[0].get('src')
        imageTitle = re.sub(invalidCharacters, '', imageLink[0].get('title'))
        imageFile = open(os.path.join('monkeyUser', os.path.basename(str(comicIndex) + "-" + imageTitle + '.png')), 'wb')
        imageRequest = requests.get(imageURL)
        for chunk in imageRequest.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        print("...Downloaded " + imageTitle)
    comicIndex += 1

print("Finished all downloads")

