class Movie:
    def __init__(self, episodes_info, title, rate, cover, cover_x, cover_y, url, playable, id, is_new):
        self.episodes_info = episodes_info
        self.title = title
        self.rate = rate
        self.cover = cover
        self.cover_x = cover_x
        self.cover_y = cover_y
        self.url = url
        self.playable = playable
        self.douban_id = id
        self.is_new = is_new

    def __str__(self) -> str:
        return f"{self.title} \t ${self.rate}"


def as_movie(dct):
    return Movie(dct['episodes_info'], dct['title'], dct['rate'], dct['cover'],
                 dct['cover_x'], dct['cover_y'], dct['url'], dct['playable'], dct['id'], dct['is_new'])


class MoviesRespons:
    def __init__(self, movies):
        self.subjects = movies

    def movies(self):
        return self.subjects


def as_moview_response(dct):
    if "subjects" in dct:
        return MoviesRespons(dct['subjects'])
    return as_movie(dct)
