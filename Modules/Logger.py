import logging
from functools import wraps

DEFAULT_LOGGER_MESSAGE_FORMAT:str   = '[%(asctime)s] [%(levelname)-8s]::  %(message)s';
DEFAULT_LOGGER_DATE_FORMAT:str      = '%m-%d-%Y %I:%M:%S %p';
DEFAULT_LOGGER_LEVEL                = logging.DEBUG;
DEFAULT_LOGGER_TEMP_FILE:str        = r'./log/temp.log';
DEFAULT_LOGGER_LOGFILE:str          = r'./log/logs.log';
DEFAULT_LOGGER_LINESIZE:int         = 100;

def getDefaultLogger(loggerName:str="default-main-logger"):    
    """Sets the default logger object for general use.
    Returns a `logging.Logger` object.
    """
    #   Sets the Logger's name according to passed parameter
    logger = logging.getLogger(loggerName);
    
    #   Creates a logfile handler
    consoleHandler = logging.StreamHandler(open(DEFAULT_LOGGER_TEMP_FILE, "w"));
    
    #   Sets the Logger's level according to constant defined above
    logger.setLevel(DEFAULT_LOGGER_LEVEL);
    
    #   Sets the Logger's formatter object according to default format
    #   defined above
    loggerFormatter = logging.Formatter(fmt=DEFAULT_LOGGER_MESSAGE_FORMAT,
                                        datefmt=DEFAULT_LOGGER_DATE_FORMAT);
    
    #   Adds the formatter to the logfile handler
    consoleHandler.setFormatter(loggerFormatter);
    
    #   Adds the logfile handler to the logger
    logger.addHandler(consoleHandler);
    
    return logger;

def endLoggingSession(sessionID:int=-1) -> None:
    """Appends the current (temporary) logfile to the permanent logfile.
    """
    try:
        with open(DEFAULT_LOGGER_TEMP_FILE, "r") as currentLogFile:
            currentLoggingSession = currentLogFile.read();
            
            with open(DEFAULT_LOGGER_LOGFILE, "a") as permanentLogFile:
                permanentLogFile.write("-" * DEFAULT_LOGGER_LINESIZE+"\n");                
                permanentLogFile.write(f"SESSION:: {sessionID}\n");
                permanentLogFile.write("-" * DEFAULT_LOGGER_LINESIZE+"\n");
                permanentLogFile.write(currentLoggingSession + "\n");
    except FileNotFoundError:
        print("Couldn't properly register current logging session to the permanent logfile");
    finally:
        print(sessionID);
        return None;