This is a simple file system/process scanner that references the ClamAV database to discover viruses.

To run this program you need to have the ClamAV daemon running.

On Windows 10 you can do this with the following steps:

Go to: https://oss.netfarm.it/clamav/ and download 64 bit build.
Extract files to the C: drive
Run "freshclam.exe"
Run "clamd.exe", this will start the ClamAV daemon

After the daemon is started, run the Scanner.exe or the Scanner.py script
