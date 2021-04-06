from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def uploadToDrive(filename):
    gauth = GoogleAuth() 
    gauth.LocalWebserverAuth()          
    drive = GoogleDrive(gauth)  

    gfile = drive.CreateFile({'parents': [{'id': '1-qG4ENBg-VNKWfCn6hZvpo8dB6AEe01Y'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(filename)
    gfile.Upload() # Upload the file.
