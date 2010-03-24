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
import math


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from PointOnEarth import PointOnEarth

class GetCircleHandler(webapp.RequestHandler):
  def post(self):
    if self.request.get('lon')=="":
      lon=0.0
    else:
      lon=float(self.request.get('lon'))
    if self.request.get('lat')=="":
      lat=0.0
    else:
      lat=float(self.request.get('lat'))
    if self.request.get('r')=="":
      r=90.0
    else:
      r=float(self.request.get('r'))
    self.response.headers['Content-Type'] = "application/vnd.google-earth.kml+xml"
    self.response.out.write("""<Folder>
    <name>KML Circle Generator Output</name>
    <visibility>1</visibility>
    <Placemark>
        <name>circle</name>
        <visibility>1</visibility>
        <Style>
            <geomColor>ff0000ff</geomColor>
            <geomScale>1</geomScale>
        </Style>
        <LineString>
            <coordinates>""")
    p=PointOnEarth(lon,lat)
    for i in range(0,361,5):
      p2=p.getPointBydirection(i,r)
      self.response.out.write('%.8f,%.8f ' % (p2.lon,p2.lat))
    self.response.out.write("""</coordinates>
        </LineString>
    </Placemark>
</Folder>""")

def main():
  application = webapp.WSGIApplication([('/circle', GetCircleHandler)],debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
