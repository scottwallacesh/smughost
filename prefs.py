#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
    def post(self):

        prefs = UserPrefs().fetch()
        try:
            prefs.api_key = self.request.get("api_key")
            prefs.nickname = self.request.get("nickname")
            prefs.app_name = self.request.get("app_name")
            prefs.put()
        except Exception, e:
            pass

        self.redirect("/")

def main():
    application = webapp.WSGIApplication([('/prefs', PrefHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
