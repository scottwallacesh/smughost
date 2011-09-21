#!/usr/bin/env python
"""Class to store and retrieve user preferences."""

__version__ = "1.0"
__author__ = "Scott Wallace <scott@wallace.sh>"

from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users

class UserPrefs(db.Model):
    """Class to fetch and store user preferences."""
    api_key = db.StringProperty(default="")
    nickname = db.StringProperty(default="")
    app_name = db.StringProperty(default="")

    def fetch(self, user_id=None):
        """Function to store the user's preferences based on their user_id()."""

        # Check for a user ID.
        if user_id is None:
            # Check to see if we're logged in.
            user = users.get_current_user()
            if user is None:
                # Nope.
                return None

            # Fetch the user ID.
            user_id = user.user_id()

        # Get the key from the DB.
        key = db.Key.from_path("UserPrefs", user_id)
        userprefs = db.get(key)

        # Check for data.
        if userprefs is None:
            # None.  Create an entry.
            userprefs = UserPrefs(key_name=user_id)

        return userprefs

class PrefHandler(webapp.RequestHandler):
    """Preferences handler."""
    def post(self):
        # Fetch our preferences object
        prefs = UserPrefs().fetch()

        try:
            # Set the variables from the form
            prefs.api_key = self.request.get("api_key")
            prefs.nickname = self.request.get("nickname")
            prefs.app_name = self.request.get("app_name")

            # Push the changes to the DB.
            prefs.put()
        except Exception, e:
            # Oops.  An error.
            self.response.out.write("There was an error storing the preferences: %s" % e)
            return

        self.redirect("/")

def main():
    """Main function for executing the script."""
    application = webapp.WSGIApplication([('/prefs', PrefHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
