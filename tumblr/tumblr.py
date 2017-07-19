#!/usr/bin/env python3

from generate import render

page = render("tumblr/tumblr.html", absolute="https://brianhouse.net")

print(page)