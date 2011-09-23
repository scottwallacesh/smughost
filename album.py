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
    def get(self, albumID, albumKey):
        """Fuction to handle GET requests."""

        # Fetch the application settings
        prefs = AppPrefs().fetch()

        # Check to see if the user preferences object has anything of value in it
        if not getattr(prefs, "api_key"):
            # Nope.  Display a simple page to explain.
            self.response.out.write("""
            <html>
                <head>
                    <title>Not configured</title>
                </head>
                <body>
                    <h1>The application is not yet configured.</h1>
                    <p>This application is not yet configured.  The administrator should visit, <a href="/prefs">/prefs</a> to configure it.</p>
                </body>
            </html>
            """)
            return

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
           imageURL = smugmug.images_getURLs(ImageID=image["id"], ImageKey=image["Key"])["Image"]
           self.response.out.write("""<div class="image">""")
           self.response.out.write("""<a href="%s">""" % (imageURL["MediumURL"]))
           self.response.out.write("""<img src="%s" />""" % (imageURL["ThumbURL"]))
           self.response.out.write("""</a>""")
           self.response.out.write("""</div>\n""")

def main():
    application = webapp.WSGIApplication([(r"/album/(.*)/(.*)", MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()