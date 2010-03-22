import math

class PointOnEarth:
    tolerance=0.000000001
    R=6371300.0
    def __init__(self,lon=0.0,lat=0.0):
        self.lon=(lon+180.0) % 360.0 -180.0
        if lat>90.0:
            self.lat=90.0
        elif lat<-90.0:
            self.lat=-90.0
        else:
            self.lat=lat
    def radToDeg(self,radian):
        return radian*180.0/math.pi
    def degToRad(self,degree):
        return math.pi*degree/180.0
    def disToRad(self,distance):
        return distance/self.R
    def radToDis(self,radian):
        return radian*self.R
    def distanceTo(self,p):
        return self.radToDis(
            math.acos(
                math.cos(
                    self.degToRad(self.lat)
                )*math.cos(
                    self.degToRad(p.lat)
                )*math.cos(
                    self.degToRad(self.lon-p.lon)
                )+math.sin(
                    self.degToRad(self.lat)
                )*math.sin(
                    self.degToRad(p.lat)
                )
            )
        )
    def getPointBydirection(self,direction,distance):
        direct=self.degToRad(direction % 360.0)
        r=self.degToRad(distance)
        lon=self.degToRad(self.lon)
        lat=self.degToRad(self.lat)
        lonDiff = 0.0
        p= PointOnEarth()
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
                cosLonDiff=(math.cos(r)-sinLatX*math.sin(lat))/(math.cos(p.lat)*math.cos(lat));
                print "%.18f,%.18f,%.18f" % (cosLonDiff,(-cosLonDiff*cosLonDiff+1.0),(self.tolerance*self.tolerance))
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
        #while p.lon>math.pi or p.lon<-math.pi:
        #    if p.lon>0.0:
        #        p.lon=p.lon-math.pi*2;
        #    else:
        #        p.lon=p.lon+math.pi*2;
        p.lon=(self.radToDeg(p.lon)+180.0) % 360.0 -180.0
        p.lat=self.radToDeg(p.lat)
        return p

if __name__=="__main__":
    p=PointOnEarth(45.0,45.0)
    print "<Folder><name>KML Circle Generator Output</name><visibility>1</visibility><Placemark><name>circle</name><visibility>1</visibility><Style><geomColor>ff0000ff</geomColor><geomScale>1</geomScale></Style><LineString><coordinates>"
    for i in range(0,361,5):
        #print "Point[%d]:" % i
        p2=p.getPointBydirection(i,p.R*math.pi/2.0)
        print "%.9f, %.9f" % (p2.lon,p2.lat)
    print "</coordinates></LineString></Placemark></Folder>"

