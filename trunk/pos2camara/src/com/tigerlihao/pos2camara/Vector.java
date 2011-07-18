package com.tigerlihao.pos2camara;

public class Vector {
	double x,y,z;
	
	public Vector(){
		this.x=1.0;
		this.y=0.0;
		this.z=0.0;
	}

	public Vector(double x,double y,double z){
		this.x=x;
		this.y=y;
		this.z=z;
	}

	
	public double getX() {
		return x;
	}

	public void setX(double x) {
		this.x = x;
	}

	public double getY() {
		return y;
	}

	public void setY(double y) {
		this.y = y;
	}

	public double getZ() {
		return z;
	}

	public void setZ(double z) {
		this.z = z;
	}
	
	public Vector toFormal(){
		double fx,fy,fz,r;
		fx=this.x;
		fy=this.y;
		fz=this.z;
		r=Math.sqrt(fx*fx+fy*fy+fz*fz);
		try{
			fx/=r;
			fy/=r;
			fz/=r;
			return new Vector(fx,fy,fz);
		}catch(Exception e){
			return new Vector();
		}
	}
	public Vector rotate(Vector v, double a){
		a=a*Math.PI/180;
		Vector k=v.toFormal();
		double cos=Math.cos(a),sin=Math.sin(a);
        double kv=k.x*this.x+k.y*this.y+k.z*this.z;
        double rx=this.x*cos+(k.y*this.z-k.z*this.y)*sin+kv*k.x*(1-cos);
        double ry=this.y*cos+(k.z*this.x-k.x*this.z)*sin+kv*k.y*(1-cos);
        double rz=this.z*cos+(k.x*this.y-k.y*this.x)*sin+kv*k.z*(1-cos);
		return new Vector(rx,ry,rz);
	}
	public void rotateTo(Vector v, double a){
		a=a*Math.PI/180;
		Vector k=v.toFormal();
		double cos=Math.cos(a),sin=Math.sin(a);
        double kv=k.x*this.x+k.y*this.y+k.z*this.z;
        double rx=this.x*cos+(k.y*this.z-k.z*this.y)*sin+kv*k.x*(1-cos);
        double ry=this.y*cos+(k.z*this.x-k.x*this.z)*sin+kv*k.y*(1-cos);
        double rz=this.z*cos+(k.x*this.y-k.y*this.x)*sin+kv*k.z*(1-cos);
		this.x=rx;
		this.y=ry;
		this.z=rz;
	}
	public String toString(){
		return("x:"+this.x+",y:"+this.y+",z:"+this.z);
	}
	public double getHeading(){
		double h=Math.atan2(this.x,this.y)*180/Math.PI;
		if(h<0)
			h+=360;
		return h;
	}
	public double getTilt(){
		double t=Math.atan2(Math.sqrt(this.x*this.x+this.y*this.y),-this.z)*180/Math.PI;
		return t;
	}
	public Vector getWing(){
		return new Vector(1,0,0).rotate(new Vector(0,0,-1), this.getHeading());
	}
	public Vector getHead(){
		return new Vector(0,1,0).rotate(new Vector(1,0,0), this.getTilt()).rotate(new Vector(0,0,-1), this.getHeading());
	}
}
