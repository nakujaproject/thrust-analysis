from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def uploadToDrive(filename):
    gauth = GoogleAuth() 
    gauth.LocalWebserverAuth()          
    drive = GoogleDrive(gauth)  

    gfile = drive.CreateFile({'parents': [{'id': '1Cp_PTI2zgyUtxkU_rm3zBI9VGqS3twwE'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(filename)
    gfile.Upload() # Upload the file.
