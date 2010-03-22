import math

class PointOnEarth:
    tolerance=0.000000001#error less than 0.1m
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
        direct=direct % 360.0
        r=math.fabs((r+180.0)%360.0-180.0)
        p= PointOnEarth()
        if 90.0-self.lat<self.tolerance:#Center Point is North Polar
            p.lon=self.lon+180.0-direct;
            p.lat=90.0-r
        elif self.lat+90.0<self.tolerance:#Center Point is South Polar
            p.lon=90.0+180.0-direct;
            p.lat=self.lat+r
        else:
	        direct=math.radians(direct)
	        r=math.radians(r)
	        lon=math.radians(self.lon)
	        lat=math.radians(self.lat)
	        lonDiff = 0.0

	        s = math.sin(r) * math.sin(r) * math.cos(direct) + math.cos(r)* math.cos(r)
	        sinLatX = (s * math.cos(lat) - math.cos(r) * math.cos(lat + r))/ math.sin(r)
	        if -sinLatX*sinLatX+1.0<self.tolerance*self.tolerance:#Object Point is polar
	            if direct>(math.pi/2) and direct<(math.pi*3/2):
	                p.lat=-math.pi/2
	            else:
	                p.lat=math.pi/2
	            lonDiff = 0.0
	        else:
	            p.lat=math.asin(sinLatX)
	            if (math.cos(lat)*math.cos(lat)<self.tolerance*self.tolerance):#Point p is polar.
	                lonDiff=math.pi-direct;
	            else:# Point p is not polar.
	                cosLonDiff1=(math.cos(r)-sinLatX*math.sin(lat))/(math.cos(p.lat)*math.cos(lat));
	                cosLonDiff=-(s * math.sin(lat) - math.cos(r) * math.sin(lat + r))/ (math.sin(r)*math.cos(p.lat));
	                print "%.18f,%.18f,%.18f,%.18f" % (cosLonDiff1,cosLonDiff,(-cosLonDiff*cosLonDiff+1.0),(self.tolerance*self.tolerance))
	                if -cosLonDiff*cosLonDiff+1.0<self.tolerance*self.tolerance:#northward or southward
	                    if cosLonDiff>0.0:
	                        lonDiff = 0.0;
	                    else:
	                        lonDiff=math.pi;
	                else:
	                    lonDiff=math.acos(cosLonDiff)
	                    if direct>math.pi:
	                        lonDiff = -lonDiff
	        print "%.12f" % lonDiff
	        p.lon=lon+lonDiff;
	        p.lon=(math.degrees(p.lon)+180.0) % 360.0 -180.0
	        p.lat=math.degrees(p.lat)
        return p

if __name__=="__main__":
    p=PointOnEarth(45.0,45.0)
    print "<Folder><name>KML Circle Generator Output</name><visibility>1</visibility><Placemark><name>circle</name><visibility>1</visibility><Style><geomColor>ff0000ff</geomColor><geomScale>1</geomScale></Style><LineString><coordinates>"
    for i in range(0,361,5):
        #print "Point[%d]:" % i
        p2=p.getPointBydirection(i,p.R*math.pi/2.0)
        print "%.9f, %.9f" % (p2.lon,p2.lat)
    print "</coordinates></LineString></Placemark></Folder>"

