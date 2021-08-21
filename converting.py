from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import docx2txt

gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there

    # This is what solved the issues:
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:

    # Refresh them if expired

    gauth.Refresh()
else:

    # Initialize the saved creds

    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")  
drive = GoogleDrive(gauth)



#Note that CreateFile() will create GoogleDriveFile instance but not actually upload a file to Google Drive.

file = drive.CreateFile({'title': 'conv.docx', 
                         'mimeType': 'application/msword'})

# Read file and set it as a content of this instance.
file.SetContentFile('lk.jpg')
file.Upload(param={'convert': True})
file.Upload() # Upload the file.
print (file)
file_id=file['id']


#downloading the doc file locally in a word format



download_file = drive.CreateFile({'id': file_id})
download_file.GetContentFile('converted.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document') 




#destroying the temporary docx file 

file.Trash()  # Move file to trash.
file.UnTrash()  # Move file out of trash.
file.Delete()  # Permanently delete the file.

# Passing docx file to process function
text = docx2txt.process("converted.docx")

# Saving content inside docx file into output.txt file
with open("output.txt", "w") as text_file:
	print(text, file=text_file)


