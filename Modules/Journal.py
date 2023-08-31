import json;

class JournalException(Exception):
    JOURNAL_EXCEPTION_EXCEPTION_PREFIX  :str="J"
    INVALID_DATE_EXCEPTION_MESSAGE      :str="invalid parameter date: ";
    INVALID_DATE_ERROR                  :int=1;
    
    def __init__(self, message, errors) -> None:
        super().__init__(message);
        self.errors = errors;

class Journal:
    DEFAULT_JOURNALS_FILEPATH:str="./Journals/";
    DEFAULT_JOURNALS_DATA_FILEPATH:str="./Journals/Data/";
    DEFAULT_JOURNAL_FILE_EXTENSION:str=".md";
    
    def __init__(self, date:str) -> None or Exception:
        self.filepath   = self.DEFAULT_JOURNALS_FILEPATH + date + self.DEFAULT_JOURNAL_FILE_EXTENSION;
        
        from os import path;
        if(path.exists(self.filepath) != True):
            self.isValid = False;
            return None;
        else:
            
            from datetime       import datetime;
            from json           import dump, load;
            
            self.isValid        = True;
            self.date           = date;
            self.file           = open(self.filepath, mode='a+');
            self.journalDict    = {
                "data": {
                    "journal-creation-date" : datetime.now().strftime("%Y-%m-%d"),
                    "date"                  : self.date,
                    "file-location"         : self.filepath,
                    "entries"               : 0,
                    "activities"            : 0,
                    "events"                : 0,
                    "aleph"                 : 0,
                    "project-developments"  : 0                    
                },
                
                "statistics": {
                    
                },
                "entries"               : [],
                "activities"            : [],
                "events"                : [],
                "aleph"                 : [],
                "project-developments"  : []
            }
            
            self.jsonFile       = open(self.filepath.replace("md", "json").replace("/Journals/", "/Journals/Data/"), "w");
            self.csvFile        = open(self.filepath.replace("md","csv").replace("/Journals/", "/Journals/Data/"), "w");
            
            
class CurrentJournal(Journal):
    def __init__(self) -> None:
        """Override the Journal.__init__() method for creating a file for the
        current date. If the file already exists, no Exception is raised and the
        __init__() method just calls super().

        Returns:
            _type_: _description_
        """
        from datetime import datetime;
        currentFormattedDate    = datetime.now().strftime("%Y-%m-%d");
        currentJournalFilepath  = Journal.DEFAULT_JOURNALS_FILEPATH + currentFormattedDate + Journal.DEFAULT_JOURNAL_FILE_EXTENSION;
        self.filepath           = currentJournalFilepath;
        
        from os import path;     
        if(path.exists(currentJournalFilepath) != True):
            self.file           = open(currentJournalFilepath, "w");
            
        return super().__init__(date=currentFormattedDate);
        
        
        