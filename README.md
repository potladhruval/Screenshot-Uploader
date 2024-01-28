# Screenshot Uploader 6.0

## Introduction
Screenshot Uploader 6.0 is a Python-based application designed to automate the process of capturing screenshots and uploading them directly to a specified Google Drive folder. It features a user-friendly graphical interface and leverages Google APIs for secure file handling.

## Features
- **Interactive GUI**: Built with `tkinter` for ease of use.
- **Screenshot Capturing**: Utilizes `PIL` (Python Imaging Library) for capturing screenshots.
- **Google Drive Integration**: Uploads screenshots to a designated Google Drive folder.
- **Clipboard Link**: Automatically copies the link of the uploaded screenshot to the clipboard for easy sharing.
- **Asynchronous Processing**: Implements threading for efficient operation.
- **Service Account Authentication**: Uses Google service account for secure API interactions.

## Requirements
This application requires Python 3.x and the following Python libraries:
- `tkinter`
- `PIL` (Pillow)
- `google-api-python-client`
- `google-auth`
- `google-auth-httplib2`
- `google-auth-oauthlib`

Install these using pip:
```bash
pip install pillow google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

## Setup
### Configuring `credentials.json`
To use this application, you'll need to create and configure your own `credentials.json` file for Google API authentication. Here's the process:

1. **Create a Google Cloud Project**: Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2. **Enable Drive API**: In the API & Services dashboard, enable the Google Drive API.
3. **Create Credentials**:
   - Navigate to "Credentials" and select "Create credentials", then "Service account".
   - Follow the instructions to create a new service account.
4. **Download JSON File**:
   - Click on your new service account.
   - Go to "Keys" tab, click "Add Key", and choose "JSON".
   - Download the JSON key file. This is your `credentials.json`.
5. **Share Drive Folder**: Share the Google Drive folder with the email address of your service account.

Place the `credentials.json` file in the same directory as the `Screenshot_Uploader6.0.py` script.

### Script Configuration
In the `Screenshot_Uploader6.0.py` script, update the `DRIVE_FOLDER_ID` constant to the ID of the Google Drive folder where you wish to upload screenshots.

## Installation and Running the Application
Ensure Python 3.x is installed on your system. Install the required libraries as mentioned in the "Requirements" section, place the `credentials.json` file in the same directory as the script, and then run the script:
```bash
python Screenshot_Uploader6.0.py
```
The application GUI will launch, allowing you to capture and upload screenshots.

## Security Note
Keep your `credentials.json` file secure and never share it publicly, as it contains sensitive information.

## Contributing
Contributions to this project are welcome. Please feel free to fork, modify, and make pull requests.
