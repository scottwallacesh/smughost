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
    def get(self):
        """Fuction to handle GET requests."""
        # Fetch the application settings
        prefs = AppPrefs().fetch()

        # Check to see if the user preferences object has anything of value in it
        if not getattr(prefs, "api_key"):
            # Nope.  Display a simple form to explain
            self.response.out.write("""
            <html>
                <head>
                    <title>Not configured</title>
                </head>
                <body>
                    <h1>The application is not yet configured.</h1>
                    <p>This webapp is not yet configured.</p>
                </body>
            </html>
            """)
            return

        # So far, so good.  Try connecting to SmugMug.
        try:
            smugmug = SmugMug(api_key=prefs.api_key, app_name=prefs.app_name)
            smugmug.login_anonymously()
            albums = smugmug.albums_get(NickName=prefs.nickname)
        except Exception, e:
            # Hmmm... something's not right.
            self.response.out.write("There was a problem connecting to SmugMug: %s" % e)
            return

        # List the albums
        for album in albums["Albums"]:
            self.response.out.write("%s, %s<br/>" % (album["id"], album["Title"]))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
