#!/usr/bin/env python3
# Copyright (c) 2017 Intel Corporation. All rights reserved.
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

from builtin_interfaces.msg import *
import math
import rclpy
from sensor_msgs.msg import *
from std_msgs.msg import *
import threading
from time import time

def main():
  rclpy.init()

  times = input('How many times do you want to run? ')
  ms = input('Please enter the period of publishing a topic in millisecond ')
  period = int(ms) / 1000
  print('The publisher will publish a JointState topic %s times every %sms.' % (times, ms))
  start = time();

  node = rclpy.create_node('endurance_publisher_rclpy')
  publisher = node.create_publisher(JointState, 'endurance_topic')
  time = Time()
  time.sec = 123456
  time.nanosec = 789
  header = Header()
  header.stamp = time
  header.frame_id = 'main_frame'
  msg = JointState()
  msg.header = header
  msg.name = ['Tom', 'Jerry']
  msg.position = [1.0, 2.0]
  msg.velocity = [2.0, 3.0]
  msg.effort = [4.0, 5.0, 6.0]
  totalTimes = int(times)
  sentTimes = 0

  def publish_topic():
    nonlocal publisher
    nonlocal msg
    nonlocal timer
    nonlocal sentTimes
    if sentTimes > totalTimes:
      timer.cancel()
      node.destroy_node()
      rclpy.shutdown()
      diff = time() - start
      milliseconds, seconds = math.modf(diff)
      print('Benchmark took %d seconds and %d milliseconds.' % (seconds, round(milliseconds * 1000)))
    else:
      publisher.publish(msg)
      sentTimes += 1
      timer = threading.Timer(period, publish_topic)
      timer.start()

  timer = threading.Timer(period, publish_topic)
  timer.start()

if __name__ == '__main__':
  main()

