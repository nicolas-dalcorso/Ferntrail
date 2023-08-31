import Modules.System as System

if __name__ == '__main__':
    mainManager = System.Manager();
    j           = mainManager.getCurrentJournal();
    print(mainManager._generateIdentifier("teste"));
    mainManager.endSystemSession();