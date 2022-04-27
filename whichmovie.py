#!/bin/env python3

from http import HTTPStatus
import json
import logging
import urllib.parse
import urllib.request

from movie import as_moview_response


class DoubleMoviePicker:
    USER_AGENT = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}

    def __init__(self) -> None:
        self.base = "https://movie.douban.com"

    def request_raw(self, path, params: map):
        kvs = [f"{k}={urllib.parse.quote(v)}" for k, v in params.items()]
        queries = "&".join(kvs)
        complete_url = f"{self.base}{path}?{queries}"
        req = urllib.request.Request(
            complete_url, headers=DoubleMoviePicker.USER_AGENT)
        with urllib.request.urlopen(req) as resp:
            if resp.status != HTTPStatus.OK:
                return (None, f"request failed: code {resp.status_code}")
            return (resp.read(), None)

    def pick_tags(self):
        return self.request_raw("/j/search_tags", {"type": "movie"})

    def pick_movie(self, tag):
        raw, fail_reason = self.request_raw(
            "/j/search_subjects", {"type": "movie", "tag": f"{tag}", "sort": "rank", "page_limit": "20", "page_start": "0"})
        if fail_reason != None:
            return (None, fail_reason)
        movies_response = json.loads(raw, object_hook=as_moview_response)
        return (movies_response.movies(), None)


def main():
    picker = DoubleMoviePicker()
    raw_tags, err_msg = picker.pick_tags()
    if err_msg != None:
        logging.error("request tags failed: %s", err_msg)
        exit(-1)

    tags = json.loads(raw_tags)

    while True:
        print("豆瓣电影tag如下：")
        for i, t in enumerate(tags["tags"]):
            print(i, "\t", t)
        tags_len = len(tags["tags"])
        try:
            user_select = input(f"选择你需要获取的电影列表(0-{tags_len})：")
            index_select = int(user_select)
            if index_select < 0 or index_select >= tags_len:
                raise ValueError()
        except ValueError:
            logging.error(
                "invalid input '%s', only '0-%d' is permited.", user_select, tags_len)
        else:
            movies, err_msg = picker.pick_movie(tags["tags"][index_select])
            if err_msg != None:
                logging.error("request movie failed: %s", err_msg)
                exit(-1)
            for i, m in enumerate(movies):
                print(i, m)
        confirm = input("\n输入 'y' 继续， 其他退出：")
        if confirm != 'y':
            break


if __name__ == "__main__":
    main()
