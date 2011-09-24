#!/usr/bin/env python

import sys
sys.path.append("lib/external/smugpy/src/")

from prefs import AppPrefs

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from smugpy import SmugMug

import xhtml

class MainHandler(webapp.RequestHandler):
     """Class to handle the main webapp functionality."""
     def get(self):
         """Fuction to handle GET requests."""
         html = xhtml.HTML(self)
 
         # Fetch the application settings
         prefs = AppPrefs().fetch()
 
         # Check to see if the user preferences object has anything of value in it
         if not getattr(prefs, "api_key"):
             self.redirect("/static/unconfig.html")
             return

         if getattr(prefs, "category"):
             self.redirect("/category/%s" % prefs.category)
             return

         html.header()
 
         # So far, so good.  Try connecting to SmugMug.
         try:
             smugmug = SmugMug(api_key=prefs.api_key, api_version="1.3.0", app_name=prefs.app_name)
             categories = smugmug.categories_get(NickName=prefs.nickname)
             albums = smugmug.albums_get(NickName=prefs.nickname)
         except Exception, e:
             # Hmmm... something's not right.
             self.response.out.write("There was a problem connecting to SmugMug: %s" % e)
             return

         # Main logic loop to display albums, images, etc.
         # List the albums.
         for category in categories["Categories"]:
             for album in albums["Albums"]:
                 count = 0
                 if album["Category"]["id"] == category["id"]:
                     count += 1

                 if count > 0:
                     self.response.out.write("""<div class="category">""")
                     self.response.out.write("""<a href="/category/%s">""" % (category["id"]))
                     self.response.out.write("""<img src="http://%s.smugmug.com/photos/random.mg?AlbumID=%s&AlbumKey=%s&Size=Thumb" alt="%s" />""" % (prefs.nickname, album["id"], album["Key"], category["NiceName"]))
                     self.response.out.write("""</a>""")
                     self.response.out.write("""<h1>%s</h1>""" % (category["NiceName"]))
                     self.response.out.write("""</div>""")

                     break;

         html.footer()

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
