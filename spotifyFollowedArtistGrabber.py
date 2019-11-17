import requests, json

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQBKM0I7LtOPNAp3NsfatPVQZGjx-LgT0ZVZyd2XpjFeuI_QTyyn2G35CtCbdYfQyIayBUqzJnjcAkVkjrSRLzzurYgrgm1VEH7dHLg5FuZAB76vlZjkiGHsBCLCgOU6Cu4RkoG2xCLAysJ88Irb0Q',
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
    name = artists[0]['name']
    print name
    return next

# getArtists('0Y5tJX1MQlPlqiwlOH1tJY')
getAllArtists()