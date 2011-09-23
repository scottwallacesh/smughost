#!/usr/bin/env python
"""Class to handle the main page of the site."""

import sys
sys.path.append("lib/external/smugpy/src/")

from prefs import AppPrefs

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from smugpy import SmugMug

class MainHandler(webapp.RequestHandler):
     """Class to handle the main webapp functionality."""
     def get(self, categoryID):
         """Fuction to handle GET requests."""
 
         # Fetch the application settings
         prefs = AppPrefs().fetch()
 
         # Check to see if the user preferences object has anything of value in it
         if not getattr(prefs, "api_key"):
             self.redirect("/static/unconfig.html")
             return
 
         # So far, so good.  Try connecting to SmugMug.
         try:
             smugmug = SmugMug(api_key=prefs.api_key, api_version="1.3.0", app_name=prefs.app_name)
             albums = smugmug.albums_get(NickName=prefs.nickname)
         except Exception, e:
             # Hmmm... something's not right.
             self.response.out.write("There was a problem connecting to SmugMug: %s" % e)
             return
 
         # Main logic loop to display albums, images, etc.
         # List the albums.
         for album in albums["Albums"]:
             if album["Category"]["id"] == int(categoryID):
                 self.response.out.write("""<div class="album">""")
                 self.response.out.write("""<a href="/album/%s/%s">""" % (album["id"], album["Key"]))
                 self.response.out.write("""<img src="http://%s.smugmug.com/photos/random.mg?AlbumID=%s&Size=Tiny&AlbumKey=%s" />""" % (prefs.nickname, album["id"], album["Key"]))
                 self.response.out.write("""</a>""")
                 self.response.out.write("""<h1>%s</h1>""" % (album["Title"]))
                 self.response.out.write("""</div>""")

def main():
    application = webapp.WSGIApplication([('/category/(.*)', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
