#!/usr/bin/env python

class HTML:
    def __init__(self, response):
        self.response = response.response

    def header(self, title="SmugHost"):
        self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%s</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css" />
</head>
<body>
    <div id="wrap">
        <div id="header"></div>
        <div id="nav"><a href="/">Photos</a></div>
        <div id="content">
\n""" % (title))

    def footer(self):
        self.response.out.write("""
        </div>
    </div>
</body>
</html>""")
