import requests, json, sys

# authToken = sys.argv[1]
authToken = "BQBGP8jV-wdIlty8GyT3O7cnCdM1LNWlzkgTvo1B-787ffD8NkHIVi3MXYXgJ_UTR380ddUnB1elDP7afEmBDipK95hLuIA4eDDzfQnVukmQlya-hILat7h6GHKQmwD2X4pvckTbtP44randnVjE1y-aZPFTaQpwe0Bgl2dYusSHp9q3BhPuNlLTYhiDovdapqRLhhgz2N9QuXD0L_BGCWOBp1VWOpE16aDvcC37W-D0UtkbqWRAkl5smWVuFm5Cfvu6dpor0kUF84c"
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
        ('offset', '1')
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
        if owner == 'bunz4dayz':
            tracks = getPlaylistTracks(id, name)


    # TODO NEED TO THEN GRAB THE NEXT BATCH OF PLAYLISTS

    return items

def getPlaylistTracks(pid, pname):

    params = (
        ('limit', '50'),
        ('offset', '1')
    )

    response = requests.get('https://api.spotify.com/v1/playlists/' + pid + '/tracks', headers=headers, params=params)

    # print json.loads(response.text)  
    print 'PLAYLIST: ' + pname

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
    with open('playlists/' + pname, 'w+') as outfp:
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
