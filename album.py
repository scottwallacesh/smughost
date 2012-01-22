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
    def get(self, albumID, albumKey):
        """Fuction to handle GET requests."""
        html = xhtml.HTML(self)

        # Fetch the application settings
        prefs = AppPrefs().fetch()

        # Check to see if the user preferences object has anything of value in it
        if not getattr(prefs, "api_key"):
            self.redirect("/static/unconfig.html")
            return

        html.header(prefs.title)

        # So far, so good.  Try connecting to SmugMug.
        try:
            smugmug = SmugMug(api_key=prefs.api_key, api_version="1.3.0", app_name=prefs.app_name)
            images = smugmug.images_get(AlbumID=albumID, AlbumKey=albumKey)
        except Exception, e:
            # Hmmm... something's not right.
            self.response.out.write("There was a problem connecting to SmugMug: %s" % e)
            return

        # Main logic loop to display albums, images, etc.
        # List the albums.
        for image in images["Album"]["Images"]:
            imageInfo = smugmug.images_getInfo(ImageID=image["id"], ImageKey=image["Key"])["Image"]

            # Try the video URL
            try:
                url = imageInfo["Video640URL"]
                rel = ""
            # Otherwise, just use the photo
            except KeyError:
                url = imageInfo["MediumURL"]
                rel = "lightbox[%s]" % albumID

            self.response.out.write("""<div class="image">""")
            self.response.out.write("""<a href="%s" rel="%s">""" % (url, rel))
            self.response.out.write("""<img src="%s" alt="%s" />""" % (imageInfo["TinyURL"], imageInfo["Caption"]))
            self.response.out.write("""</a>""")
            self.response.out.write("""<h3>%s</h3>""" % (imageInfo["Caption"]))

            self.response.out.write("""</div>\n""")

        html.footer()

def main():
    application = webapp.WSGIApplication([(r"/album/(.*)/(.*)", MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
