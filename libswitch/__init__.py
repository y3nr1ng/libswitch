import logging

# Create the logger.
logger = logging.getLogger('libswitch')
logger.setLevel(logging.DEBUG)

# Create a file handler which logs the debug messages.
#fh = logging.FileHandler('libswitch.log')
#fh.setLevel(logging.DEBUG)

# Create a console handler.
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create the formatter and add it to the handlers.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Finally, add the handlers to the logger.
#logger.addHandler(fh)
logger.addHandler(ch)
