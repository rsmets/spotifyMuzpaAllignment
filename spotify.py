import requests, json, sys, os

auth_token = sys.argv[1]
action = sys.argv[2]

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    "Authorization": "Bearer " + auth_token,
}

# ensure the playlist directory is created
path = "./playlists"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

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

def getAllPlaylistsByOwner(playlistOwner):
    offset = 0
    total_grabbed = 0
    params = (
        ('limit', '50'),
        ('offset', str(offset))
    )

    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers, params=params)

    print json.loads(response.text)  

    responseJson = json.loads(response.text) 
    
    playlistCount = responseJson['total']

    while total_grabbed < playlistCount:
        getPlaylists(playlistOwner, offset)
        offset = offset + 50
        total_grabbed = total_grabbed + 50

def getPlaylists(playlistOwner, offset):

    params = (
        ('limit', '50'),
        ('offset', str(offset))
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
        # if 'Johan' in owner:
        if playlistOwner in owner:
            getPlaylistTracks(id, name)

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
   

if action == 'artists':
    getAllArtists() # for grabbing followed artists and dumping them in artistNames.json & artistInfoPretty.json files
elif action == 'all_playlists':
    playlist_owner = sys.argv[3]
    getAllPlaylistsByOwner(playlist_owner) # for grabbing all playlist tracks from target owner and dumping them in ./playlists/<playlist_name>/<track_names>
elif action == 'playlist':
    playlist_name = sys.argv[3]
    playlist_id = sys.argv[4]
    getPlaylistTracks(playlist_id, playlist_name) # for grabbing all playlist tracks from target owner and dumping them in ./playlists/<playlist_name>/<track_names>
