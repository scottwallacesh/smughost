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
import sys
sys.path.append("lib/external/smugpy/src/")

from prefs import UserPrefs

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from smugpy import SmugMug

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            # Nope.  Go login.
            self.redirect(users.create_login_url(self.request.path))
            return

        prefs = UserPrefs().fetch()
        if not getattr(prefs, "api_key"):
            # Display a form to capture the data
            self.response.out.write("""
            <html>
                <head>
                    <title>Edit prefs</title>
                </head>
                <body>
                    <form action="/prefs" method="post">
                        <label for="api_key">SmugMug API Key</label>
                        <input type="text" id="api_key" name="api_key" />
                        <label for="nickname">SmugMug Username</label>
                        <input type="text" id="nickname" name="nickname" />
                        <label for="app_name">SmugMug API App Name</label>
                        <input type="text" id="app_name" name="app_name" />

                        <input type="submit" value="submit" />
                    </form>
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
            self.response.out.write("There was a problem connecting to SmugMug: %s" % e)
            return

        # List te albums
        for album in albums["Albums"]:
            self.response.out.write("%s, %s<br/>" % (album["id"], album["Title"]))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
