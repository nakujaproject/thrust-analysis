from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def uploadToDrive(filename):
    gauth = GoogleAuth() 
    gauth.LocalWebserverAuth()          
    drive = GoogleDrive(gauth)  

    gfile = drive.CreateFile({'parents': [{'id': '1_XFmlOkCpjbi8vf_rz7UfW3jZmPQDh1f'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(filename)
    gfile.Upload() # Upload the file.
