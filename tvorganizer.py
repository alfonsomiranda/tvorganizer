import sys
import re
import os
import config
import shutil
import smtplib

compiled_regexs = []
mail_text = ""

def cleanRegexedSeriesName(seriesname):
    seriesname = re.sub("(\D)[.](\D)", "\\1 \\2", seriesname)
    seriesname = re.sub("(\D)[.]", "\\1 ", seriesname)
    seriesname = re.sub("[.](\D)", " \\1", seriesname)
    seriesname = seriesname.replace("_", " ")
    seriesname = re.sub("-$", "", seriesname)
    return seriesname.strip()

def compileRegexs():
    for cpattern in config.filename_patterns:
        cregex = re.compile(cpattern, re.VERBOSE)
        compiled_regexs.append(cregex)

def parse(name, filename):
    global mail_text
    for cmatcher in compiled_regexs:
        match = cmatcher.match(name)
        if match:
            namegroups = match.groupdict().keys()
            seriesname = match.group('seriesname')
            #print match.group('seasonnumber')
            #print match.group('episodenumber')
            seriesname = cleanRegexedSeriesName(seriesname)
            path = filename
	    if os.path.exists(path):
                try:
                    if not os.path.exists(config.destination_dir + seriesname + '/'):
                        os.makedirs(config.destination_dir + seriesname + '/')
                    destinationPath = config.destination_dir + seriesname + '/' + name
                    print "Moving " + path
                    shutil.move(path, destinationPath)
                    mail_text = mail_text + "<li>Moved <b>" + path + "</b> to <b>"+ destinationPath + "</b></li>"
                except IOError as (errno, strerror):
                    errorType = "I/O error({0}): {1}".format(errno, strerror)
                    print errorType
                    mail_text = mail_text + "<p>Error " + path + ": "+ errorType + "</p>"
                break

def sendMail():
    global mail_text
 
    subject = 'tvorganizer'
    body = mail_text
 
    headers = ["From: " + config.MAIL_SENDER,
           "Subject: " + subject,
           "To: " + config.MAIL_RECIPIENT,
           "MIME-Version: 1.0",
           "Content-Type: text/html"]
    headers = "\r\n".join(headers)
 
    session = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
 
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(config.MAIL_SENDER, config.MAIL_PASSWORD)
 
    session.sendmail(config.MAIL_SENDER, config.MAIL_RECIPIENT, headers + "\r\n\r\n" + body)
    session.quit()
    mail_text = ""

if __name__ == "__main__":
    compileRegexs()
    for root, subFolders, files in os.walk(config.origin_dir):
        for file in files:
            f = os.path.join(root,file)
            if file.endswith(('.mp4', '.avi', '.mkv', '.srt')):
                parse(file,f)

    if (mail_text != ""):
        sendMail()
