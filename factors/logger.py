import logging.handlers

class Logger:

 logger = None

 levels = {'n' : logging.NOTSET,
  'd' : logging.DEBUG,
  'i' : logging.INFO,
  'w' : logging.WARN,
  'e' : logging.ERROR,
  'c' : logging.CRITICAL}

 def __init__(self,log_level = 'n', log_file_path = 'default_log.log',log_max_byte = 10 * 1024 * 1024,log_backup_count = 5):
  self.log_level = log_level
  self.log_file_path = log_file_path
  self.log_max_byte = log_max_byte
  self.log_backup_count = log_backup_count

  Logger.logger = logging.Logger('oggingmodule.FinalLogger')
  log_handler = logging.handlers.RotatingFileHandler(filename=self.log_file_path,
                                                     maxBytes=self.log_max_byte,
                                                     backupCount=self.log_backup_count)
  log_fmt = logging.Formatter('[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s')
  log_handler.setFormatter(log_fmt)
  Logger.logger.addHandler(log_handler)
  Logger.logger.setLevel(Logger.levels.get(self.log_level))

 @staticmethod
 def getLogger():
  if Logger.logger is not None:
   return Logger.logger

  return Logger.logger

if __name__ == '__main__':
 logger = Logger.getLogger()
 # logger.debug('this is a debug msg!')
 # logger.info('this is a info msg!')
 # logger.warning('this is a warn msg!')
 # logger.error('this is a error msg!')
 # logger.critical('this is a critical msg!')
