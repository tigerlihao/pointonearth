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

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.response.out.write('<Folder><name>KML Circle Generator Output</name><visibility>1</visibility><Placemark><name>circle</name><visibility>1</visibility><Style><geomColor>ff0000ff</geomColor><geomScale>1</geomScale></Style><LineString><coordinates>')
    p=PointOnEarth(45.0,85.0)
    #p2=p.getPointBydirection(0,4.0)
    #p3=p.getPointBydirection(360,0.0)
    #self.response.out.write('%.12f, %.12f ' % (p2.lon,p2.lat))
    #self.response.out.write('%.12f, %.12f ' % (p3.lon,p3.lat))
    for i in range(0,361,3):
        p2=p.getPointBydirection(i,0.001)
        self.response.out.write('%.6f,%.6f ' % (p2.lon,p2.lat))
    self.response.out.write('</coordinates></LineString></Placemark></Folder>')

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
