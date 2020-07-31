import requests, json

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    # 'Authorization': 'Bearer BQCTaJoji7nUjyDaYGZlfeJnFr9w1bWLuNfi6fO8LvTcM_IClEKchRMkZXTGzckwwT9HLqay6JCuLzX_CmJDVB1t1id_KqeyPvk68YyhCiKxyASuYV3fisuQIOXkbHhyKtjvfQs_Wgy-U06z-dWmyQ',
    "Authorization": "Bearer BQAHYdRweompKPkKWjhT1JJ6tRc6vgomQ5tR0pirrQtyDUYV-1lkBx-FwForUd4v3Ohy9oeiolGqy-_0dy-shB1jQyPx3m_MLS5EQ4_IDar7X0bUnkqBnl45vwtEggc4ycvuWmxH1OIAWm8_uFTqww",
}

def getAllArtists():
    total = 0
    nextUuid = getArtists(None)
    while (nextUuid):
        nextUuid = getArtists(nextUuid)

def getArtists(afterUuid):

    params = (
        ('type', 'artist'),
        ('limit', '50'),
    )

    if afterUuid:
        params = (
            ('type', 'artist'),
            ('after', afterUuid),
            ('limit', '50'),
        )

    response = requests.get('https://api.spotify.com/v1/me/following', headers=headers, params=params)

    # print json.loads(response.text) 

    responseJson = json.loads(response.text) 
    
    next = responseJson['artists']['cursors']['after']
    print next
    print responseJson['artists']['total']

    artists = responseJson['artists']['items']
    writeArtistsInfoToFile(artists)
    writeArtistsNamesToFile(artists)

    name = artists[0]['name']
    print name
    return next

def writeArtistsInfoToFile(artists):
    with open('artistInfoPretty.json', 'a+') as outfp:
        # outfp.write(json.dumps(artists))
        outfp.write(json.dumps(artists, sort_keys=True, indent=4, separators=(',', ': ')))

def writeArtistsNamesToFile(artists):
    with open('artistNames.json', 'a+') as outfp:
        for a in artists:
            outfp.write((a['name'].encode('utf-8').replace('"', '')))
            outfp.write('\r\n')
   

# getArtists('0Y5tJX1MQlPlqiwlOH1tJY')
getAllArtists()
