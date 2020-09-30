def tracklist(**kwargs):
    for artist, albums in kwargs.items():
        print(artist)
        for album, track in albums.items():
            print('ALBUM: {0} TRACK: {1}'.format(album, track))

