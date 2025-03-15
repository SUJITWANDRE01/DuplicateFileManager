"""
DuplicateFileRemoval.py - Automated duplicate file detection and removal utility

This script scans a specified directory for duplicate files based on MD5 checksums,
removes duplicates, logs the operations, and emails reports at regular intervals.

Features:
- Identifies duplicate files using MD5 hash comparison
- Automatically removes duplicate files (keeps the first occurrence)
- Creates timestamped log files of all operations
- Runs at user-defined intervals
- Emails log reports with operation statistics

Usage:
    python DuplicateFileRemoval.py <directory_path> <time_interval_minutes> <email>

Example:
    python DuplicateFileRemoval.py E:/Data/Demo 50 user@example.com
"""

############################################################################################################
#
# Import required modules
#
############################################################################################################
import os                                     # For file and directory operations
import hashlib                                # For generating file checksums
import time                                   # For timing operations and creating timestamps
import smtplib                                # For sending emails
import urllib.request                         # For checking internet connectivity
import urllib.error                           # For handling network errors
import sys                                    # For accessing command line arguments
from email import encoders                    # For encoding email attachments
from email.mime.text import MIMEText          # For creating email text content
from email.mime.base import MIMEBase          # For email attachments
from email.mime.multipart import MIMEMultipart # For creating multi-part emails



############################################################################################################
#
# Check if the system has an active internet connection.
# Returns True if connected to the internet, False otherwise
#
############################################################################################################
def is_connected():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=5)
        return True
    except urllib.error.URLError:
        return False



############################################################################################################
#
# Send an email with the log file and operation statistics.
# Args:
#   log_path (str): Path to the log file to attach
#   start_time (str): Time when scanning started
#   total_scanned (int): Total number of files scanned
#   total_duplicates (int): Total number of duplicate files found
#   send_to (str): Recipient's email address
#
############################################################################################################
def send_mail(log_path, start_time, total_scanned, total_duplicates, send_to):
    fromaddr = "Sender Mail ID"  # Replace with your email
    password = "Sender Password"  # Replace with your email password
    toaddr = send_to

    # Create the email message container
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Duplicate File Removal Log - " + time.ctime()

    # Create email body with operation statistics
    body = f"""
    Hello,

    Log file is created at: {time.ctime()}

    Starting time of scanning: {start_time}
    Total number of files scanned: {total_scanned}
    Total number of duplicate files found: {total_duplicates}

    This is an auto-generated mail.
    """

    # Attach the text body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Open and attach the log file
    with open(log_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(log_path)}")
        msg.attach(part)

    try:
        # Connect to Outlook's SMTP server and send the email
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print("Log file successfully sent through mail")
    except Exception as e:
        print(f"Unable to send mail. Error: {e}")



############################################################################################################
#
# Delete all duplicate files, keeping only the first occurrence.
# Args:
#   duplicates (dict): Dictionary mapping file hashes to lists of file paths
# Returns:
#   list: List of deleted file paths
#
############################################################################################################
def delete_files(duplicates):
    deleted_files = []
    for file_list in duplicates.values():
        # Keep the first file (index 0) and delete all others
        if len(file_list) > 1:
            for file in file_list[1:]:
                os.remove(file)
                deleted_files.append(file)
    return deleted_files



############################################################################################################
#
# Generate MD5 hash for a file by reading it in chunks.
# Args:
#   path (str): Path to the file
#   blocksize (int): Size of chunks to read at once
# Returns:
#   str: Hexadecimal digest of the file's MD5 hash
#
############################################################################################################
def hash_file(path, blocksize=1024):
    hasher = hashlib.md5()
    with open(path, 'rb') as file:
        buf = file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(blocksize)
    return hasher.hexdigest()



############################################################################################################
#
# Scan a directory recursively to find duplicate files based on their hash.
# Args:
#   directory (str): Path to the directory to scan
# Returns:
#   dict: Dictionary mapping file hashes to lists of file paths
#
############################################################################################################
def find_duplicates(directory):
    duplicates = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            filehash = hash_file(filepath)
            if filehash in duplicates:
                duplicates[filehash].append(filepath)
            else:
                duplicates[filehash] = [filepath]
    return duplicates



############################################################################################################
#
# Create a log file with the list of deleted files.
# Args:
#   deleted_files (list): List of paths to deleted files
#   log_dir (str): Directory where the log file should be created
# Returns:
#   str: Path to the created log file
#
############################################################################################################
def create_log(deleted_files, log_dir):
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create timestamped log filename
    log_filename = f"Log_{time.strftime('%Y%m%d%H%M%S')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    # Write log file with headers and list of deleted files
    with open(log_path, 'w') as log_file:
        log_file.write("Duplicate File Removal Log\n")
        log_file.write(f"Log created at: {time.ctime()}\n")
        log_file.write("-" * 80 + "\n")
        for file in deleted_files:
            log_file.write(f"{file}\n")
    return log_path



############################################################################################################
#
# Main function to control the flow of the duplicate file removal operation.
#
############################################################################################################
def main():
    # Validate command line arguments
    if len(sys.argv) != 4:
        print("Usage: DuplicateFileRemoval.py <directory_path> <time_interval_minutes> <email>")
        sys.exit(1)

    # Parse command line arguments
    directory_path = sys.argv[1]
    time_interval_minutes = int(sys.argv[2])
    email = sys.argv[3]

    # Convert to absolute path if relative path is provided
    if not os.path.isabs(directory_path):
        directory_path = os.path.abspath(directory_path)

    # Validate directory path
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print("Invalid directory path")
        sys.exit(1)

    # Main operational loop
    while True:
        # Record start time
        start_time = time.ctime()
        
        # Find duplicate files
        duplicates = find_duplicates(directory_path)
        total_scanned = sum(len(files) for files in duplicates.values())
        
        # Delete duplicates and create log
        deleted_files = delete_files(duplicates)
        total_duplicates = len(deleted_files)
        log_dir = "Marvellous"
        log_path = create_log(deleted_files, log_dir)

        # Send email if internet is available
        if is_connected():
            send_mail(log_path, start_time, total_scanned, total_duplicates, email)
        else:
            print("No internet connection. Unable to send email.")

        # Wait for the specified interval before next scan
        time.sleep(time_interval_minutes * 60)



if __name__ == "__main__":
    main()

