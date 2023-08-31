import Modules.Logger as log
import Modules.Journal as Journal
import os;
import json;
from collections import namedtuple;

class ManagerException(Exception):
    MANAGER_EXCEPTION_EXCEPTION_PREFIX  :str="MS"
    INVALID_IDENTIFIER_QUERY            :str="Invalid identifier query: couldn't find '{}' in system dictionary."    
    INVALID_IDENTIFIER_ERROR            :int=1;
    
    def __init__(self, message, errors) -> None:
        super().__init__(message);
        self.errors = errors;


class Manager:
    #   Filepath constants
    IDFILE_DEFAULT_SYSTEM_FILEPATH:     str=r"./Data/ids.json";
    JOURNALFILE_DEFAULT_SYSTEM_FILEPATH:str=r"./Data/journals.json";
    
    #   Dictionaries constants
    ID_DEFAULT_SYSTEM_DICT:             dict={
        "sessions"      : 0,
        "registry"      : {
            "activities"            : 0,
            "events"                : 0,
            "journal-entries"       : 0,
            "aleph-entries"         : 0,
            "project-developments"  : 0
        }
    }
    
    JOURNAL_DEFAULT_SYSTEM_DICT:        dict={
        "entries-quantity"  : 0,
        "entries"           : [],
        "current-session"   : {
            "actions"               : [],
            "initialization-time"   : ""
        }
    }
    
    _FILEPATHS:list=[
        IDFILE_DEFAULT_SYSTEM_FILEPATH,
        JOURNALFILE_DEFAULT_SYSTEM_FILEPATH
    ];
    
    _DICTIONARIES:list=[
        ID_DEFAULT_SYSTEM_DICT,
        JOURNAL_DEFAULT_SYSTEM_DICT
    ];
    
    #   Data constants
    Activity            = namedtuple('Activity', "id timeInitial timeEnd name description commentaries");
    ProjectDevelopment  = namedtuple('ProjectDevelopment', "id timeInitial timeEnd projectName developmentDescription commentaries");
    
    
    def getLogger(self, loggerName) -> log.logging.Logger:
        return log.getDefaultLogger(loggerName);
    
    def endLoggingSession(self) -> None:
        return log.endLoggingSession(self._generateIdentifier("sessions"));
    
    def endSystemSession(self) -> None:
        #   Ends logging session
        self.endLoggingSession();
        
        #   Updates the JSON files
        for i in range(len(self._FILEPATHS)):
            with open(self._FILEPATHS[i], "w") as f:
                json.dump(self.dicts[i], f);
    
    def checkFiles(self) -> int:
        count:int=0;
        
        for i in range(len(self._FILEPATHS)):
            curr = self._FILEPATHS[i];
            
            if(os.path.exists(curr) == False):
                try:
                    file = open(curr, "w");
                    json.dump(self._DICTIONARIES[i], file);
                    print(file.read());
                except Exception:
                    self.logger.error(f"func `{self.checkFiles.__name__}()`: Couldn't create file `{curr}`.");
                    continue;
                finally:
                    count+=1;
                    self.logger.info(f"func `{self.checkFiles.__name__}()`: Created file `{curr}`.");
        
        return count;
    
    def __init__(self, mode:str="default", 
                 loggerName:str="default-main-logger") -> None:
        
        if(mode=='default'):
            self.logger = self.getLogger(loggerName);
            self.files  = self._FILEPATHS;
            
            #   Create files if necessary
            if(self.checkFiles() == 0):
                self.logger.debug(f"func `System.{self.__init__.__name__}()`: all System files already existent.")
            
            #   Load system dictionaries
            self.ids        = json.loads(open(self.files[0], "r").read());
            self.journals   = json.loads(open(self.files[1], "r").read());
            
            self.dicts      = [self.ids, self.journals];
            
        self.buffer = "";
    
    def findKeys(self, node, keyValue):
        if(isinstance(node, list)):
            for i in node:
                for j in self.findKeys(i, keyValue):
                    yield j;
        elif(isinstance(node, dict)):
            if keyValue in node:
                yield node[keyValue];
            for k in node.values():
                for x in self.findKeys(k, keyValue):
                    yield x;
    
    def _generateIdentifier(self, identifierKey:str) -> int or None:
        if(identifierKey in self.dicts[0]["registry"].keys()):
            #   Logging
            self.logger.info(f"Retrieved identifier from system dict and incremented it: {self.dicts[0]['registry'][identifierKey]} -> {self.dicts[0]['registry'][identifierKey]}");            
            
            self.dicts[0]["registry"][identifierKey] += 1;
            return self.dicts[0]["registry"][identifierKey];
        else:
            #   Logging
            self.logger.error(f"SystemManager function `System.{self._generateIdentifier.__name__}()` raised an Exception:");
            self.logger.error(f"Couldn't retrieve identifier from system dict: '{identifierKey}'");
            self.logger.error(f"(ERROR {ManagerException.MANAGER_EXCEPTION_EXCEPTION_PREFIX}-{ManagerException.INVALID_IDENTIFIER_ERROR}): {ManagerException.INVALID_IDENTIFIER_QUERY.format(identifierKey)}");
            raise ManagerException(message=ManagerException.INVALID_IDENTIFIER_QUERY.format(identifierKey),
                                   errors=ManagerException.INVALID_IDENTIFIER_ERROR);
            return None;
        
    def newActivity(self, activityList:list) -> Activity:
        return self.Activity._make(activityList);
    
    def getCurrentJournal(self) -> Journal.CurrentJournal:
        return Journal.CurrentJournal();
    