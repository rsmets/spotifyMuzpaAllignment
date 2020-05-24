import requests, json, sys

authToken = sys.argv[1]
# authToken = "BQBrieGF1N2Egav3n5rYMV5WBVx8XjOFZ7KuDnYTVmUYDKjSGMrvVKrflCX1k-I9QZ5HX4YJRHs5N2aBxhHXqudiDQbF6k0RuYe8GlppwimUeVNqn3I_Y1wjaGOuf81jNy8iZu6BMt5KW0QZHLJt9es79MEGBgS7LQoBtoYeVH5lSznGs1on1NBqR-oSQ8wQbNGxlwTU6_UJEUIHU1T3q3XseHmTaIMxgG4bVfcTxodgl5_pFSsTtWyKvlzQkwaOsg5hR4eyA6sDMwk"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    "Authorization": "Bearer " + authToken,
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

    print json.loads(response.text)  

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

def getPlaylists():

    params = (
        ('limit', '50'),
        ('offset', '50')
    )

    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers, params=params)

    print json.loads(response.text)  

    responseJson = json.loads(response.text) 
    
    items = responseJson['items']
    # print next

    for item in items:
        name = item['name']
        id = item['id']
        owner = item['owner']['display_name']
        # if owner == 'bunz4dayz':
        if 'Johan' in owner:
            tracks = getPlaylistTracks(id, name)


    # # TODO NEED TO THEN GRAB THE NEXT BATCH OF PLAYLISTS

    # return items

def getPlaylistTracks(pid, pname):

    offset = 0
    total_grabbed = 0
    params = (
        ('limit', '50'),
        ('offset', str(offset))
    )
    

    response = requests.get('https://api.spotify.com/v1/playlists/' + pid + '/tracks', headers=headers, params=params)

    # print json.loads(response.text)  
    print 'PLAYLIST: ' + pname

    responseJson = json.loads(response.text) 
    print responseJson['total']
    totalTracks = responseJson['total']

    while total_grabbed < totalTracks:
        getPlaylistTracksHelper(pid, pname, offset)
        offset = offset + 50
        total_grabbed = total_grabbed + 50
    
def getPlaylistTracksHelper(pid, pname, offset):
    
    params = (
        ('limit', '50'),
        ('offset', str(offset))
    )

    response = requests.get('https://api.spotify.com/v1/playlists/' + pid + '/tracks', headers=headers, params=params)
    responseJson = json.loads(response.text) 
    items = responseJson['items']

    # # print next

    writePlayInfoToFiles(pname, items)

    # for item in items:
    #     name = item['track']['name']
    #     # id = item['id']
    #     # tracks = getPlaylistTracks(id)
    #     # href = item['href']
    #     print name


    return "items"
    
def writePlayInfoToFiles(pname, tracks):
    pname = pname.replace(' ', '_')
    # with open('playlists/' + pname, 'w+') as outfp:
    with open('playlists/' + pname, 'a+') as outfp: # use to append to a playlist track file
        for track in tracks:
            name = track['track']['name']
            atrist = track['track']['artists'][0]['name']
            print name
            outfp.write(atrist.encode('utf-8').replace('"', ''))
            outfp.write(' ~ ')
            outfp.write(name.encode('utf-8').replace('"', ''))
            outfp.write('\r\n')

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
# getAllArtists()

getPlaylists()

# BQD3O5Din4szXaSGM_LGVcG6OwWaaXs-ovSvms47ivLaEE9KvnQViXKmW7wToSSxVwZ1DzRMQpTNgQ0mkSEoKK1QFhiTEReyqNHRsbiFuEJ32wCyqA-7KalUdkPjkVHlMbd4bMsFqaQ8-ZXSgckwMCENRhqiElFW2YC7hRsHYy3xHf7eBGX17JLHiy8JBKw3bAxFbRmZNaICIeu5mscgTtKYIgmdYa0FfHXIucVUPlQeMkTK1g1AFTMFqQHwasvLcTRCxFureK14B5M
