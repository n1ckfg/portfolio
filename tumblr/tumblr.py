#!/usr/bin/env python3

from generate import render

page = render("tumblr/tumblr.html", absolute="http://brianhouse.net")

print(page)