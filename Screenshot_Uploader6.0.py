import os
import time
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from PIL import ImageGrab
import threading
import pytz

# Constants
DRIVE_FOLDER_ID = "1IgoWyws2a8iVwvqrMfRF9BEvAXb4udUW"  # Replace with your folder ID

# Global variable to store the time of the last screenshot
last_screenshot_time = None

# Global variable to store the last five screenshot links along with timestamps
last_five_screenshots = []

class CaptureScreenshotError(Exception):
    pass

class DriveUploadError(Exception):
    pass

def capture_screenshot():
    try:
        # Hide the root window
        root.withdraw()
        root.update()

        # Wait for a moment to let the window disappear
        time.sleep(1)

        # Capture the screen
        screenshot = ImageGrab.grab()

        # Show the root window
        root.deiconify()

        # Save the captured screen as a temporary file
        screenshot_file = 'screenshot.png'
        screenshot.save(screenshot_file)

        # Explicitly close the file to release resources
        screenshot.close()

        return screenshot_file
    except Exception as e:
        raise CaptureScreenshotError(f"Error capturing screenshot: {str(e)}")

def upload_to_drive(file_path):
    try:
        # Authenticate using the service account credentials
        credentials = service_account.Credentials.from_service_account_file('credentials.json')
        drive_service = build('drive', 'v3', credentials=credentials)

        # Upload the captured image to Google Drive
        file_metadata = {
            'name': 'screenshot.png',
            'parents': [DRIVE_FOLDER_ID]
        }

        media = MediaFileUpload(file_path, mimetype='image/png', resumable=True)
        request = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        )

        # Execute the request
        uploaded_file = request.execute()

        return uploaded_file
    except Exception as e:
        raise DriveUploadError(f"Error uploading to Google Drive: {str(e)}")

def handle_upload_completion(link, screenshot_file):
    global last_screenshot_time, last_five_screenshots  # Add these lines to access the global variables

    try:
        # Extract the file ID from the Google Drive link
        file_id = link.split('=')[-1]

        # Convert the timestamp to CST (Central Standard Time)
        timestamp_cst = datetime.now(pytz.timezone("America/Chicago")).strftime("%Y-%m-%d %I:%M:%S:%p")

        # Build a valid filename using the file ID and timestamp
        local_screenshot_file = 'screenshot.png'

        # Combine the link and timestamp
        link_with_timestamp = f"{link} - {timestamp_cst}"

        # Update the list of the last five screenshots with only the latest link
        last_five_screenshots.insert(0, link_with_timestamp)
        last_five_screenshots = last_five_screenshots[:5]

        # Update the GUI with the last five links and timestamps
        screenshot_text.delete(1.0, END)
        screenshot_text.insert(END, "\n".join(last_five_screenshots))

        # Display the time since the last screenshot as a counter
        update_time_counter()

        # Clear the clipboard and append only the link without the timestamp
        root.clipboard_clear()
        root.clipboard_append(link)
        root.update()

        # Check if the file exists before removing
        if os.path.exists(local_screenshot_file):
            # Clean up temporary files
            os.remove(local_screenshot_file)
        else:
            print(f"File '{local_screenshot_file}' not found.")

        # Show success message
        messagebox.showinfo("Success", "File uploaded and link copied to clipboard.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while handling upload completion: {str(e)}")


def update_time_counter():
    global last_screenshot_time  # Add this line to access the global variable

    if last_screenshot_time:
        time_difference = datetime.now() - last_screenshot_time
        seconds = time_difference.seconds

        # Display the time since the last screenshot as a counter
        if seconds <= 30:
            time_label.config(text=f"Seconds since last screenshot: {seconds}", fg="black")
        else:
            minutes = seconds // 60
            time_label.config(text=f"Minutes since last screenshot: {minutes}", fg="red")

        # Schedule the next update after 1 second
        root.after(1000, update_time_counter)
    else:
        time_label.config(text="No previous screenshots")

def threaded_capture_and_upload():
    global last_screenshot_time  # Add this line to access the global variable
    # Disable the capture button during the upload process
    capture_button.config(state=DISABLED)

    try:
        # Inform the user that the screenshot is being captured
        status_label.config(text="Capturing screenshot...", fg="blue")
        root.update()

        screenshot_file = capture_screenshot()

        # Update the time of the last screenshot
        last_screenshot_time = datetime.now()

        # Inform the user that the screenshot is being uploaded
        status_label.config(text="Uploading screenshot...", fg="blue")
        root.update()

        uploaded_file = upload_to_drive(screenshot_file)
        link = f"https://drive.google.com/open?id={uploaded_file['id']}"
        handle_upload_completion(link, screenshot_file)
    except CaptureScreenshotError as e:
        messagebox.showerror("Error", f"An error occurred while capturing screenshot: {str(e)}")
    except DriveUploadError as e:
        messagebox.showerror("Error", f"An error occurred while uploading to Google Drive: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    finally:
        # Re-enable the capture button after the upload process is complete
        capture_button.config(state=NORMAL)
        # Reset the status label
        status_label.config(text="", fg="black")

# Create the GUI window
root = Tk()
root.title("Screenshot Uploader")

# Create and configure GUI elements
capture_button = Button(root, text="Capture and Upload", command=threaded_capture_and_upload)
capture_button.pack(pady=20)

status_label = Label(root, text="", font=("Helvetica", 12))
status_label.pack()

time_label = Label(root, text="", font=("Helvetica", 10))
time_label.pack()

screenshot_text = Text(root, height=6, width=50)
screenshot_text.pack()

# Start the GUI main loop
root.mainloop()
