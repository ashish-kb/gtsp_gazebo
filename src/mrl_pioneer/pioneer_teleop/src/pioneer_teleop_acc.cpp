
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>

class TeleopPioneer
{
public:
  TeleopPioneer();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);
  
  ros::NodeHandle nh_;

  int linear_, angular_;
  double l_scale_, a_scale_, vel_inct;
  ros::Publisher vel_pub_;
  ros::Subscriber joy_sub_;
  
};

TeleopPioneer::TeleopPioneer():
  linear_(1),
  angular_(2),
  a_scale_(0.5),
  l_scale_(0.2),  
  vel_inct(0.0)  
{

  nh_.param("axis_linear", linear_, linear_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);
  
  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/ROSARIA/cmd_vel", 1);  
  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopPioneer::joyCallback, this);

}

void TeleopPioneer::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{

  geometry_msgs::Twist vel;
  
  if (joy->buttons[4])
	vel_inct = vel_inct + 0.005;

  if (joy->buttons[5])
	vel_inct = vel_inct - 0.005;
  
  if (vel_inct<0)
        vel_inct = 0.0;  
  
  vel.angular.z = (a_scale_+vel_inct)*joy->axes[angular_];  
  vel.linear.x = (l_scale_+vel_inct)*joy->axes[linear_];

  vel_pub_.publish(vel);
  //ROS_INFO("Publiquei (ANG=%f, LIN=%f)", vel.angular.z, vel.linear.x);  
  //ROS_INFO("Publiquei INC=%f", vel_inct);    
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "pioneer_teleop");
  TeleopPioneer teleop_turtle;

  ros::spin();
}
