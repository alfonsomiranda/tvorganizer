# tvorganizer

tvorganizer is a small script that organize a folder with series in a destination folder, sorted by the different series.

# Configuration

Set this parameters in the file config.py:

- Origin_dir -> source directory
- Destination_dir -> destination directory, which must be different from before.

If you want receive an email whenever you move a file or have an error, you must complete the following parameters:

- SMTP_SERVER = "YOUR_SMTP_SERVER"
- SMTP_PORT = 587 #MAIL PORT
- MAIL_SENDER = "MAIL_SENDER"
- MAIL_RECIPIENT = "MAIL_RECIPIENT"
- MAIL_PASSWORD = "PASSWORD"

# Usage

You just have to launch the following command.

```
python tvorganizer/tvorganizer.py
```

# Contributors

Filename patterns from https://github.com/dbr/tvnamer/tree/master/tvnamer
