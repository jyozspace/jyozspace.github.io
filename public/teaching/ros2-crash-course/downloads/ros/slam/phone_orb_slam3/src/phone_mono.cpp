// SPDX-License-Identifier: GPL-3.0-or-later
// Course adapter to ORB-SLAM3's public API. Native IMU components are inspection topics; this adapter uses images.
#include <cmath>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include <Eigen/Geometry>
#include "rclcpp/rclcpp.hpp"
#include "cv_bridge/cv_bridge.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/path.hpp"
#include "std_msgs/msg/string.hpp"
#include "System.h"
#include "MapPoint.h"

class PhoneMono : public rclcpp::Node {
public:
  PhoneMono() : Node("phone_mono") {
    const auto vocabulary = declare_parameter<std::string>("vocabulary", "");
    const auto settings = declare_parameter<std::string>("settings", "");
    output_ = declare_parameter<std::string>("keyframe_output", "phone-keyframes.txt");
    if(vocabulary.empty() || settings.empty()) throw std::runtime_error("Pass real vocabulary and calibrated settings paths");
    cv::FileStorage config(settings, cv::FileStorage::READ);
    if(!config.isOpened()) throw std::runtime_error("Cannot open calibrated ORB settings");
    width_ = static_cast<int>(config["Camera.width"]);
    height_ = static_cast<int>(config["Camera.height"]);
    double fx = static_cast<double>(config["Camera1.fx"]);
    if(width_<=0 || height_<=0 || !std::isfinite(fx) || fx<=0) throw std::runtime_error("Invalid camera dimensions or focal length");
    config.release();
    slam_ = std::make_unique<ORB_SLAM3::System>(vocabulary, settings, ORB_SLAM3::System::MONOCULAR, true);
    pose_ = create_publisher<geometry_msgs::msg::PoseStamped>("/phone/slam/camera_pose", 5);
    cloud_ = create_publisher<sensor_msgs::msg::PointCloud2>("/phone/slam/tracked_points", 2);
    path_ = create_publisher<nav_msgs::msg::Path>("/phone/slam/path", 2);
    status_ = create_publisher<std_msgs::msg::String>("/phone/slam/status", 5);
    subscription_ = create_subscription<sensor_msgs::msg::Image>("/phone/camera/image_raw", rclcpp::SensorDataQoS().keep_last(2),
      [this](sensor_msgs::msg::Image::ConstSharedPtr image){ process(image); });
    RCLCPP_INFO(get_logger(), "Monocular map has arbitrary scale. Pangolin shows the optimized sparse map; ROS cloud contains currently tracked points only.");
  }
  ~PhoneMono() override {
    if(slam_) {slam_->Shutdown(); if(!output_.empty()) slam_->SaveKeyFrameTrajectoryTUM(output_);}
  }
private:
  void process(const sensor_msgs::msg::Image::ConstSharedPtr & image) {
    if(static_cast<int>(image->width)!=width_ || static_cast<int>(image->height)!=height_) {
      RCLCPP_ERROR_THROTTLE(get_logger(), *get_clock(), 2000, "Phone resolution changed. Restore calibrated mode and restart mapping."); return;
    }
    const double time=rclcpp::Time(image->header.stamp).seconds();
    if(time<=last_time_) return;
    try {
      const auto pixels=cv_bridge::toCvShare(image, "bgr8");
      const auto Tcw=slam_->TrackMonocular(pixels->image,time);
      last_time_=time;
      const int tracking=slam_->GetTrackingState();
      std_msgs::msg::String report; report.data="ORB tracking state="+std::to_string(tracking)+" (2=OK); units=arbitrary monocular scale";status_->publish(report);
      if(tracking!=2) {history_.poses.clear();return;}
      const auto Twc=Tcw.inverse();
      const Eigen::Vector3f t=Twc.translation();
      const Eigen::Quaternionf q(Twc.rotationMatrix());
      geometry_msgs::msg::PoseStamped pose;
      pose.header=image->header;pose.header.frame_id="phone_slam_world";
      pose.pose.position.x=t.x();pose.pose.position.y=t.y();pose.pose.position.z=t.z();
      pose.pose.orientation.x=q.x();pose.pose.orientation.y=q.y();pose.pose.orientation.z=q.z();pose.pose.orientation.w=q.w();pose_->publish(pose);
      // Diagnostic pose history is bounded and not retroactively loop-optimized.
      history_.header=pose.header;history_.poses.push_back(pose);
      if(history_.poses.size()>2000) history_.poses.erase(history_.poses.begin());
      path_->publish(history_);
      std::vector<Eigen::Vector3f> points;
      for(auto *point:slam_->GetTrackedMapPoints()) if(point && !point->isBad()) {
        const auto p=point->GetWorldPos();if(p.allFinite())points.push_back(p);
      }
      sensor_msgs::msg::PointCloud2 cloud;cloud.header=pose.header;
      sensor_msgs::PointCloud2Modifier modifier(cloud);modifier.setPointCloud2FieldsByString(1,"xyz");modifier.resize(points.size());
      if(!points.empty()) {
        sensor_msgs::PointCloud2Iterator<float> x(cloud,"x"),y(cloud,"y"),z(cloud,"z");
        for(const auto &p:points){*x=p.x();*y=p.y();*z=p.z();++x;++y;++z;}
      }
      cloud_->publish(cloud);
    } catch(const cv_bridge::Exception &e){RCLCPP_ERROR(get_logger(),"Image conversion: %s",e.what());}
  }
  std::unique_ptr<ORB_SLAM3::System> slam_;
  std::string output_;int width_=0,height_=0;double last_time_=-1;
  nav_msgs::msg::Path history_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr pose_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr cloud_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_;
};
int main(int argc,char **argv){rclcpp::init(argc,argv);try{rclcpp::spin(std::make_shared<PhoneMono>());}catch(const std::exception &e){RCLCPP_ERROR(rclcpp::get_logger("phone_mono"),"%s",e.what());if(rclcpp::ok())rclcpp::shutdown();return 1;}if(rclcpp::ok())rclcpp::shutdown();return 0;}
