import logging
loggingLevel = logging.INFO
projName = 'AirspaceNFT'
projDir = f'Z:\\workspace3\\{projName}\\'
logFile = f'{projDir}{projName}.log'
# https://docs.python.org/3.9/howto/logging.html#logging-to-a-file
# https://stackoverflow.com/questions/6290739/python-logging-use-milliseconds-in-time-format
# logging.basicConfig(filename=logFile, encoding='utf-8', format='%(asctime)s.%(msecs)03d\t%(name)s\t%(levelname)s\t%(message)s',datefmt='%Y-%m-%d,%H:%M:%S', level=loggingLevel)

logging.basicConfig(filename=logFile, encoding='utf-8', format='%(asctime)s.%(msecs)03d\t%(name)s\t%(levelname)s\t%(message)s',datefmt='%m-%d %H:%M:%S', level=loggingLevel)


from brownie import network
activeNet = network.show_active()

