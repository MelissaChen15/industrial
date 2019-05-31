import logging.handlers

class Logger:

 logger = None

 levels = {"n" : logging.NOTSET,
  "d" : logging.DEBUG,
  "i" : logging.INFO,
  "w" : logging.WARN,
  "e" : logging.ERROR,
  "c" : logging.CRITICAL}

 log_level = "n"
 log_file = "update_factors.log"
 log_max_byte = 10 * 1024 * 1024
 log_backup_count = 5

 @staticmethod
 def getLogger():
  if Logger.logger is not None:
   return Logger.logger

  Logger.logger = logging.Logger("oggingmodule.FinalLogger")
  log_handler = logging.handlers.RotatingFileHandler(filename = Logger.log_file,
                                                     maxBytes = Logger.log_max_byte,
                                                     backupCount = Logger.log_backup_count)
  log_fmt = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
  log_handler.setFormatter(log_fmt)
  Logger.logger.addHandler(log_handler)
  Logger.logger.setLevel(Logger.levels.get(Logger.log_level))
  return Logger.logger

def print1():
 print(1)

def return1():
 return 1



if __name__ == "__main__":
 logger = Logger.getLogger()
 # logger.debug("this is a debug msg!")
 # logger.info("this is a info msg!")
 # logger.warning("this is a warn msg!")
 # logger.error("this is a error msg!")
 # logger.critical("this is a critical msg!")
 logger.info(return1())

