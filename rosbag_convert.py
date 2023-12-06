import subprocess
import yaml
import rosbag
import cv2
from cv_bridge import CvBridge
import numpy as np


# FILENAME = 'wchinv1'
FILENAME = 'outdoor2'
# FILENAME = 'rooster_2020-03-10-11-39-38_1'
ROOT_DIR = '/home/zhangyanyu'
BAG_DIR = '/home/zhangyanyu'
BAGFILE = BAG_DIR + '/' + FILENAME + '.bag'
timestamps = []


if __name__ == '__main__':
    bag = rosbag.Bag(BAGFILE)
    for i in range(2):
        if (i == 0):
            # TOPIC = '/carla/ego_vehicle/rgb_left/image'
            TOPIC = '/zed2i/zed_node/left/image_rect_color'
            # TOPIC = '/camera/infra1/image_rect_raw'
            DESCRIPTION = 'left_'

        else:
            # TOPIC = '/carla/ego_vehicle/rgb_right/image'
            TOPIC = '/zed2i/zed_node/right/image_rect_color'
            # TOPIC = '/camera/infra2/image_rect_raw'
            DESCRIPTION = 'right_'
        image_topic = bag.read_messages(TOPIC)
        # l=0
        for k, b in enumerate(image_topic):
            
            bridge = CvBridge()
            cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
            cv_image.astype(np.uint8)
            
            # timesecond = int(b.timestamp.to_sec() *1e9)
            # if(timesecond %10 == 0):
            # if(k %10 == 0):
            if (DESCRIPTION == 'left_'):
                # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(cv_image, alpha=0.03), cv2.COLORMAP_JET)
                cv2.imwrite(ROOT_DIR + '/image_0/' +  str(b.timestamp) + '.png', cv_image)
                timestamps.append(b.timestamp)
            else:

                cv2.imwrite(ROOT_DIR + '/image_1/' + str(timestamps[k]) + '.png', cv_image)
                # cv2.imwrite(ROOT_DIR + '/image_1/' + str(b.timestamp) + '.png', cv_image)
            
            print('saved: ' + DESCRIPTION + str(b.timestamp) + '.png')

            # l +=1
            # if(l==10):
            #     l =0


    bag.close()
    
    with open(ROOT_DIR + '/times.txt','w') as timestamp_file:
        for timestamp in timestamps:
            timestamp_file.write(str(timestamp) + '\n')
    
    print('PROCESS COMPLETE')