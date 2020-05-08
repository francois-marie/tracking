import logging
import tracking.motion_detection as modet
import tracking.homography
import tracking.heat_map

# file to be run to execute the different libs



def main():

    logging.basicConfig(filename='main.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')



    logging.info('Finished')

if __name__ == "__main__":
    main()