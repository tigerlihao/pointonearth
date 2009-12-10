package cn.tigerlihao.sphere;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

public class CircleOnSphere {
	/**
	 * The radius of the earth.
	 */
	static final double RADIUS_OF_EARTH = 6371300.0;
	/**
	 * The center of the circle, in degree.
	 */
	private Point center;
	/**
	 * The radius of the center of the circle, in meter.
	 */
	private double radius;

	/**
	 * @param lonA
	 *            the longitude of point A, in degree.
	 * @param latA
	 *            the latitude of point A, in degree.
	 * @param lonB
	 *            the longitude of point B, in degree.
	 * @param latB
	 *            the latitude of point B, in degree.
	 * @return the distanceBetween A() and B() on sphere, in meter.
	 */
	static double distanceBetween(Point a, Point b) {
		return distanceInRadian(degreeToRadian(a.lon), degreeToRadian(a.lat),
				degreeToRadian(b.lon), degreeToRadian(b.lat))
				* RADIUS_OF_EARTH;
	}

	/**
	 * @param lonA
	 *            the longitude of point A, in radian.
	 * @param latA
	 *            the latitude of point A, in radian.
	 * @param lonB
	 *            the longitude of point B, in radian.
	 * @param latB
	 *            the latitude of point B, in radian.
	 * @return the distanceBetween A() and B() on sphere, in radian.
	 */
	static double distanceInRadian(double lonA, double latA, double lonB,
			double latB) {
		return Math.acos(Math.cos(latA) * Math.cos(latB)
				* Math.cos(lonA - lonB) + Math.sin(latA) * Math.sin(latB));
	}

	/**
	 * Change degree to radian
	 * 
	 * @param degree
	 * @return radian
	 */
	static double degreeToRadian(double degree) {
		return Math.PI * degree / 180.0;
	}

	/**
	 * Change distance on earth to radian
	 * 
	 * @param distance
	 * @return radian
	 */
	static double distanceToRadian(double distance) {
		return distance / RADIUS_OF_EARTH;
	}

	/**
	 * Change radian to degree
	 * 
	 * @param radian
	 * @return degree
	 */
	static double radianToDegree(double radian) {
		return 180.0 * radian / Math.PI;
	}

	/**
	 * Change radian to distance on earth
	 * 
	 * @param radian
	 * @return distance
	 */
	static double radianToDistance(double radian) {
		return RADIUS_OF_EARTH * radian;
	}

	/**
	 * constructor of this class without parameters.
	 */
	public CircleOnSphere() {
		this.center.lon = 0;
		this.center.lat = 0;
		this.radius = 0;
	}

	/**
	 * initiate the circle with center point and radius.
	 * 
	 * @param lon
	 *            the longitude of the center of circle, in degree.
	 * @param lat
	 *            the latitude of the center of circle, in degree.
	 * @param distance
	 */
	public CircleOnSphere(Point a, double radius) {
		this.center = a;
		this.radius = radius;
	}

	/**
	 * initiate the circle with center point and another point on circle.
	 * 
	 * @param lonA
	 * @param latA
	 * @param lonP
	 * @param latP
	 */
	public CircleOnSphere(Point a, Point b) {
		this.center = a;
		this.radius = distanceBetween(a, b);
	}

	public double getRadius() {
		return radius;
	}

	public Point getCenter() {
		return center;
	}

	public void setRadius(double distance) {
		this.radius = distance;
	}

	public void setCenter(Point center) {
		this.center = center;
	}

	public static Point getPointByDirection(Point p, double direction,
			double distance) {
		double r = distanceToRadian(distance);
		double lat = degreeToRadian(p.lat);
		double lon = degreeToRadian(p.lon);
		double direct = degreeToRadian(direction);
		double lonX;
		double latX;
		double dLonX;
		double s = Math.sin(r) * Math.sin(r) * Math.cos(direct) + Math.cos(r)
				* Math.cos(r);
		double sinLatX = (s * Math.cos(lat) - Math.cos(r) * Math.cos(lat + r))
				/ Math.sin(r);
		if (-sinLatX * sinLatX + 1 < 0.0000000001) {//Object point is polar.
			if (direct > (Math.PI / 2) && direct < (Math.PI * 3 / 2)) {
				latX = -Math.PI / 2;
			} else {
				latX = Math.PI / 2;
			}
			dLonX = 0.0;
		} else {//Object point is not polar.
			latX = Math.asin(sinLatX);
			if (Math.cos(lat) * Math.cos(lat) < 0.0000000001) {//Point p is polar.
				dLonX = Math.PI - direct;
			} else {//Point p is not polar.
				double cosdLonX = (Math.cos(r) - Math.sin(latX) * Math.sin(lat))
						/ (Math.cos(latX) * Math.cos(lat));
				if (-cosdLonX * cosdLonX + 1 < 0.0000000001) {//differant in long is 0 or 180.0. 
					if(cosdLonX>0.0){
						dLonX = 0.0;
					}else{
						dLonX = Math.PI;
					}
				} else {
					dLonX = Math.acos(cosdLonX);
					if (direct > Math.PI) {
						dLonX = -dLonX;
					}
				}
			}
		}
		lonX = lon + dLonX;
		while (lonX > Math.PI || lonX < -Math.PI) {
			if (lonX > 0.0) {
				lonX = lonX - Math.PI * 2;
			} else {
				lonX = lonX + Math.PI * 2;
			}
		}
		return new Point(radianToDegree(lonX), radianToDegree(latX));
	}

	public List<Point> getCirclePoints() {
		List<Point> points = new ArrayList<Point>();
		for (int i = 0; i <= 360; i++) {
			points.add(getPointByDirection(this.center, i, this.radius));
		}
		return points;
	}

	public static void main(String[] args) throws Exception {
		// System.out.println(getPointByDirection(new Point(0.0, -89.0), 0.0,
		// 10000));
		CircleOnSphere c = new CircleOnSphere(new Point(123.999, 30.0), RADIUS_OF_EARTH*Math.PI/2);
		List<Point> points = c.getCirclePoints();
		System.out.println("<Folder>");
		System.out.println("<name>KML Circle Generator Output</name>");
		System.out.println("<visibility>1</visibility>");
		System.out.println("<Placemark>");
		System.out.println("<name>circle</name>");
		System.out.println("<visibility>1</visibility>");
		System.out.println("<Style>");
		System.out.println("<geomColor>ff0000ff</geomColor>");
		System.out.println("<geomScale>1</geomScale>");
		System.out.println("</Style>");
		System.out.println("<LineString>");
		System.out.println("<coordinates>");

		for (Point point : points) {
			System.out.println(point);
		}
		System.out.println("</coordinates>");
		System.out.println("</LineString>");
		System.out.println("</Placemark>");
		System.out.println("</Folder>");

		// System.out.print(distanceBetween(new Point(30.0, 30.0),new Point(
		// 45.0, 45.0)));
	}
}

class Point {
	static final DecimalFormat FORMAT = new DecimalFormat("##0.000000000");
	double lon;
	double lat;

	Point() {
	}

	Point(double lon, double lat) {
		this.lon = lon;
		this.lat = lat;
	}

	public String toString() {
		return (FORMAT.format(this.lon) + ", " + FORMAT.format(this.lat));
	}
}
