#!/usr/bin/env python
"""Class to store and retrieve user preferences."""

from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users

class AppPrefs(db.Model):
    """Class to fetch and store user preferences."""
    api_key = db.StringProperty(default="")
    nickname = db.StringProperty(default="")
    app_name = db.StringProperty(default="")

    def fetch(self):
        """Function to fetch the application preferences."""
        # Get the key from the DB.
        key = db.Key.from_path("AppPrefs", "AppPrefs")
        appPrefs = db.get(key)

        # Check for data.
        if appPrefs is None:
            # None.  Create an entry.
            appPrefs = AppPrefs(key_name="AppPrefs")

        return appPrefs

class PrefHandler(webapp.RequestHandler):
    """Preferences handler."""
    def get(self):
        # Fetch any existing preferences.
        prefs = AppPrefs().fetch()

        # Display a form to add/update the application settings.
        self.response.out.write("""
            <html>
                <head>
                    <title>Edit prefs</title>
                </head>
                <body>
                    <h1>Edit preferences</h1>
                    <form action="/prefs" method="post">
                        <label for="api_key">SmugMug API Key</label>
                        <input type="text" id="api_key" name="api_key" value="%s" /> <br/>
                        <label for="nickname">SmugMug Username</label>
                        <input type="text" id="nickname" name="nickname" value="%s" /> <br/>
                        <label for="app_name">SmugMug API App Name</label>
                        <input type="text" id="app_name" name="app_name" value="%s" /> <br/>

                        <input type="submit" value="submit" />
                    </form>
                </body>
            </html>
            """ % (prefs.api_key, prefs.nickname, prefs.app_name))
        return


    def post(self):
        """Function to store the settings provided in the <form ...> in the get() function."""
        # Fetch our preferences object
        prefs = AppPrefs().fetch()

        try:
            # Use the variables from the form
            prefs.api_key = self.request.get("api_key")
            prefs.nickname = self.request.get("nickname")
            prefs.app_name = self.request.get("app_name")

            # Push the changes to the DB.
            prefs.put()
        except Exception, e:
            # Oops.  An error.
            self.response.out.write("There was an error storing the preferences: %s" % e)
            return

        # Back to the main page
        self.redirect("/")

def main():
    """Main function for executing the script."""
    application = webapp.WSGIApplication([('/prefs', PrefHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
