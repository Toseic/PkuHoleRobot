from interaction import inacFrame
from log import Logger
from robot import Robot




def main():
    logger = Logger()
    print("Welcome.")
    logger.info("Robot open.")
    robot = Robot(logger)

    
    inacFrame(robot)
    


if __name__ == '__main__':
    
    # print(type(logger))
    # logger.debug('this is a logger debug message')
    # logger.info('this is a logger info message')
    # logger.warning('this is a logger warning message')
    # logger.error('this is a logger error message')
    # logger.critical('this is a logger critical message')

    main()