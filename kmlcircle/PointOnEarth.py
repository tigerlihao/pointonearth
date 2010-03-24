import math

class PointOnEarth:
    tolerance=1e-9#error less than 0.1m
    tolerance2=1e-18
    R=6371300.0
    def __init__(self,lon=0.0,lat=0.0):
        self.lon=(lon+180.0) % 360.0 -180.0
        self.lat=math.fabs((lat+270.0)%360.0-180.0)-90.0
    def disToRad(self,distance):
        return distance/self.R
    def radToDis(self,radian):
        return radian*self.R
    def distanceTo(self,p):
        return self.radToDis(
            math.acos(
                math.cos(
                    math.radians(self.lat)
                )*math.cos(
                    math.radians(p.lat)
                )*math.cos(
                    math.radians(self.lon-p.lon)
                )+math.sin(
                    math.radians(self.lat)
                )*math.sin(
                    math.radians(p.lat)
                )
            )
        )
    def getPointBydirection(self,direct,r):
        direct=direct % 360.0#direction is in [0.0,360.0)
        r=r % 360.0#radium is in [0.0,360.0)
        p=PointOnEarth()#target point
        if r<self.tolerance or (360.0-r)<self.tolerance:#radium is 0.0
            p.lon=self.lon
            p.lat=self.lat
        elif math.fabs(r-180.0)<self.tolerance:#radium is 180.0
            p.lon=self.lon % 360.0 - 180.0
            p.lat=-self.lat
        elif 90.0-self.lat<self.tolerance:#Center Point is North Polar
            p.lon=self.lon+180.0-direct
            p.lat=90.0-r
        elif self.lat+90.0<self.tolerance:#Center Point is South Polar
            p.lon=self.lon+direct
            p.lat=-90.0+r
        elif direct<self.tolerance or (360.0-direct)<self.tolerance:#direction is north
            p.lat=(self.lat+r-90.0)%360.0
            if p.lat<180.0:
                p.lat=90.0-p.lat
                p.lon=self.lon % 360.0 - 180.0
            else:
                p.lat=p.lat-270.0
                p.lon=self.lon
        elif math.fabs(direct-180.0)<self.tolerance:#direction is south
            p.lat=(self.lat-r-90.0)%360.0
            if p.lat<180.0:
                p.lat=90.0-p.lat
                p.lon=self.lon % 360.0 - 180.0
            else:
                p.lat=p.lat-270.0
                p.lon=self.lon
        else:#other case
	        direct=math.radians(direct)
	        r=math.radians(r)
	        lon=math.radians(self.lon)
	        lat=math.radians(self.lat)
	        lonDiff = 0.0
	        s = math.sin(r) * math.sin(r) * math.cos(direct) + math.cos(r)* math.cos(r)
	        sinLatX = (s * math.cos(lat) - math.cos(r) * math.cos(lat + r))/ math.sin(r)
	        if -sinLatX*sinLatX+1.0<self.tolerance2:#make sure sinLatX is in(-1,1)
	            if direct>(math.pi/2) and direct<(math.pi*3/2):
	                p.lat=-math.pi/2
	            else:
	                p.lat=math.pi/2
	            lonDiff = 0.0
	        else:
	            p.lat=math.asin(sinLatX)
	            if math.cos(lat)*math.cos(lat)<self.tolerance2:#cos(lat) less than 1e-9
	                lonDiff=math.pi-direct
	            else:# Point p is not polar.
	                cosLonDiff=(math.cos(r)-sinLatX*math.sin(lat))/(math.cos(p.lat)*math.cos(lat))
	                if -cosLonDiff*cosLonDiff+1.0<self.tolerance2:#make sure cosLonDiff is in(-1,1)
	                    if cosLonDiff>0.0:
	                        lonDiff = 0.0
	                    else:
	                        lonDiff=math.pi
	                else:
	                    lonDiff=math.acos(cosLonDiff)
	                    if direct>math.pi:
	                        lonDiff = -lonDiff
	        p.lon=lon+lonDiff
	        p.lon=(math.degrees(p.lon)+180.0) % 360.0 -180.0
	        p.lat=math.degrees(p.lat)
        return p

if __name__=="__main__":
    p=PointOnEarth(45.0,45.0)
    print "<Folder>"
    print "<name>KML Circle Generator Output</name>"
    print "<visibility>1</visibility>"
    print "<Placemark>"
    print "<name>circle(%.9f, %.9f)</name>" % (p.lon,p.lat)
    print "<visibility>1</visibility>"
    print "<Style><geomColor>ff0000ff</geomColor><geomScale>1</geomScale></Style>"
    print "<LineString><coordinates>"
    for i in range(0,361,5):
        p2=p.getPointBydirection(i,90.0)
        print "%.9f, %.9f" % (p2.lon,p2.lat)
    print "</coordinates></LineString></Placemark></Folder>"

