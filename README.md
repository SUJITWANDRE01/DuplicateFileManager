# DuplicateFileManager

An automated Python utility that identifies and removes duplicate files from specified directories based on file checksums. The utility creates logs of all removed files and can email these logs at scheduled intervals.

## Features

- Identifies duplicate files using MD5 hash comparison
- Automatically removes duplicate files, keeping only the first instance
- Creates timestamped log files of all removed duplicates
- Runs at user-defined intervals (specified in minutes)
- **Automated email reporting system** that sends detailed operation statistics
- Smart connectivity detection to handle offline scenarios
- Includes comprehensive email reports with file statistics and log attachments
- Maintains all logs in a dedicated directory

## Requirements

- Python 3.x
- Internet connection (for email functionality)
- Valid email account credentials
- SMTP access (configured for Outlook by default)

## Installation

Clone this repository:
```
git clone https://github.com/SUJITWANDRE01/DuplicateFileManager.git
cd DuplicateFileManager
```

## Usage

Run the script with the following command line arguments:

```
python DuplicateFileRemoval.py <directory_path> <time_interval_minutes> <email>
```

### Parameters:

- `<directory_path>`: Absolute path of the directory to scan for duplicates
- `<time_interval_minutes>`: Time interval (in minutes) between scans
- `<email>`: Email address to send the log reports to

### Example:

```
python DuplicateFileRemoval.py E:/Data/Demo 50 recipient@example.com
```

This will:
1. Scan the E:/Data/Demo directory for duplicate files
2. Remove any duplicates found
3. Create a log file in the Marvellous directory
4. Send the log file to recipient@example.com
5. Repeat the process every 50 minutes

## Automated Email System

The program includes a robust email delivery system that:

- Automatically checks for internet connectivity before attempting to send
- Sends detailed operation reports with every scan
- Attaches the complete log file containing names of all deleted files
- Uses secure SMTP connection (configured for Outlook by default)
- Can be easily modified to use other email providers

### Email Reports Include:

- Timestamp of when the log was created
- Starting time of the scan operation
- Total number of files scanned
- Total number of duplicate files found and removed
- Complete log file as an attachment

## Important Notes

- **Before first use**: Update the email sender credentials in the `send_mail()` function
- The program keeps the first occurrence of each file and deletes subsequent duplicates
- All deleted files are logged but cannot be recovered by the program
- The utility automatically handles connection issues and will continue scanning even when offline

## License

[MIT License](LICENSE)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.
