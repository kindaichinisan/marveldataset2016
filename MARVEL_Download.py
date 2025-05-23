from bs4 import BeautifulSoup
# from urllib2 import urlopen
import urllib.request
from PIL import Image
import traceback
import threading
import datetime
import logging
import codecs
import math
import sys
import os
import io
import http.client

##Uncomment the related dat file ('VesselClassification.dat' for Vessel Classification, 'IMOTrainAndTest.dat' for Vessel Verification/Retrieval/Recognition tasks.)
FILE_TO_DOWNLOAD_FROM = "VesselClassification_no_duplicate.dat"
##FILE_TO_DOWNLOAD_FROM = "IMOTrainAndTest.dat" 

NUMBER_OF_WORKERS = 10
MAX_NUM_OF_FILES_IN_FOLDER = 5000
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256
ORIGINAL_SIZE = 1 #0 # 1 for yes, 0 for no
JUST_IMAGE = 0 #1 # 1 for yes, 0 for no


photoDetails = ["Photographer:","Title:","Captured:","IMO:","Photo Category:","Description:"]
vesselIdentification = ["Name:","IMO:","Flag:","MMSI:","Callsign:"]
technicalData = ["Vessel type:","Gross tonnage:","Summer DWT:","Length:","Beam:","Draught:"]
additionalInformation = ["Home port:","Class society:","Build year:","Builder (*):","Owner:","Manager:"]
aisInformation = ["Last known position:","Status:","Speed, course (heading):","Destination:","Last update:","Source:"]
impText = photoDetails + vesselIdentification + technicalData + additionalInformation  
impText2 = ["Former name(s):"]

sourceLink = "http://www.shipspotting.com/gallery/photo.php?lid="

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', handlers=[
    logging.FileHandler("download.log", mode="w", encoding="utf-8"),
    logging.StreamHandler() #keeps showing logs in console too
] )
logging.debug("Process started at " + str(datetime.datetime.now()))

def save_image(ID,justImage,outFolder):
    url = sourceLink + ID
    # url = "https://www.shipspotting.com/photos/gallery?imo=9300398"
    # html = urllib.request.urlopen(url,timeout = 300).read()
    print(f'url: {url}')
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=300).read()
    soup = BeautifulSoup(html,"lxml")

    images = [img for img in soup.find_all('img')]
    image_links = [each.get('src') for each in images]
    # Dictionary to store extracted info
    info = {}
    # List of fields you want to extract
    fields_to_extract = [
        "Photographer", "Title", "Photo Category", "Added", "Views", "Image Resolution", "Description", "Current name", "Current flag", "Home port", "Callsign", "IMO", "MMSI", "Build year", "Builder", "Manager", "Owner", "Class society", "Vessel Type", "Gross tonnage", "Summer DWT", "Length", "Beam", "Draught", "Photos", "Former name"
    ]
    info = {field: "" for field in fields_to_extract}

    if not justImage:
        #WJ: this is obsolete and website does not use this to pass information
        # tags = [tr for tr in soup.find_all('td')]
        # tr_text = [each.getText() for each in tags]

        #WJ: this is new way of passing information
        # Find all title-value pairs
        items = soup.find_all("div", class_="information-item")
        for item in items:
            title_span = item.find("span", class_="information-item__title")
            value_span = item.find("span", class_="information-item__value")
            if title_span and value_span:
                title = title_span.get_text(strip=True).replace(":", "")
                value = value_span.get_text(strip=True)
                info[title] = value

        #get descriptions in Photo details
        desc_div = soup.find("div", class_="summary-photo__card-photo__desc-container")
        if desc_div:
            description = desc_div.get_text(strip=True)
            info['Description']=description

        #get Former name in Vessel particulars
        former_name_container = soup.find("div", class_="summary-photo__card-general__former-name__container")
        if former_name_container:
            name_tag = former_name_container.find("a")
            info['Former name']= name_tag.get_text(strip=True) if name_tag else ""
            
        # Example output
        # for key, val in info.items():
        #     print(f"{key}: {val}")

    filename = " "
    for each in image_links:
        if each is not None and "https" in each and "jpg" in each and "photos/big" in each:
            filename=each.split('/')[-1]
            filename=filename.split('?')[0] #change 3608498.jpg?cb=0 to 3608498.jpg
            # f = urllib.request.urlopen(each)
            img_req = urllib.request.Request(each, headers={"User-Agent": "Mozilla/5.0"})

            read_complete=False
            try:
                f = urllib.request.urlopen(img_req)
                img_data = f.read()
                read_complete=True
            except http.client.IncompleteRead as e:
                logging.debug(str(ID) + f"\t - http.client.IncompleteRead for {url}")

            if read_complete:
                # Open image from bytes
                img = Image.open(io.BytesIO(img_data))

                # Crop bottom 20 pixels
                width, height = img.size
                cropped_img = img.crop((0, 0, width, height - 20))
                with open(os.path.join(outFolder, filename), "wb") as out:
                    cropped_img.save(out, "JPEG")
                if ORIGINAL_SIZE == 0:
                    img = Image.open(os.path.join(outFolder,filename)).resize((IMAGE_HEIGHT,IMAGE_WIDTH), Image.LANCZOS)
                    os.remove(os.path.join(outFolder,filename))
                    with open(os.path.join(outFolder,filename), "wb") as out:
                        img.save(out,"JPEG")
            break
        
    if filename != " " and not justImage:
        textFile = filename.split('.')[0]
        tFile = codecs.open(os.path.join(outFolder,filename)+'.dat','w','utf-8')    
        # for index,each in enumerate(tr_text):
        #     for impT in impText:
        #         if impT == each:
        #             tFile.write(each + ' ' + tr_text[index+1] + '\n')
        #             break
        # for index,each in enumerate(tr_text):
        #     for impT in impText2:
        #         if impT == each:
        #             for ind in range(1,20):
        #                 if tr_text[index+ind] != "":
        #                     tFile.write(each + ' ' + tr_text[index+ind] + '\n')
        #                 else:
        #                     break
        #             break
        tFile.write(f"url: {url}\n")
        for field in fields_to_extract:
            
            tFile.write(f"{field}: {info[field]}\n")
        tFile.close()
    if filename == " ":
        return 0
    else:
        return 1


def worker(content,workerNo):
    workerIndex = 0
    folderIndex = 0
    folderNo = 1
    currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
    if not os.path.exists(currFolder):
        os.mkdir(currFolder)
    for ID in content:
        if folderIndex == MAX_NUM_OF_FILES_IN_FOLDER:
            folderIndex = 0
            folderNo = folderNo + 1
            currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
            if not os.path.exists(currFolder):
                os.mkdir(currFolder)
        try:
            status = save_image(ID,JUST_IMAGE,currFolder)
            workerIndex = workerIndex + 1
            if status == 1:
                folderIndex = folderIndex + 1
                logging.debug(str(ID) + "\t - Downloaded... - " + str(workerIndex) + "\t/" + str(len(content)))
            else:
                logging.debug(str(ID) + "\t - NO SUCH FILE  - " + str(workerIndex) + "\t/" + str(len(content)))
        # except:
        #     traceback.print_exc()
        except Exception as e:
            logging.exception(f"❌ Error while processing ID {ID} at index {workerIndex} - {e}")

    logging.debug(str(datetime.datetime.now()) + "-------------- DONE ")

    return

priorFiles = []
dirs = os.listdir(os.getcwd())
for eachDir in dirs:
    if 'W' in eachDir:
        oldFiles = os.listdir(os.path.join(os.getcwd(),eachDir))
        for eachFile in oldFiles:
            if ".jpg" in eachFile:
                oldID = eachFile.split(".")[0]
                priorFiles.append(oldID)

downloadFile = codecs.open(FILE_TO_DOWNLOAD_FROM,"r","utf-8")
downloadContent = downloadFile.readlines()
downloadFile.close()
finalContent = []
for index,eachLine in enumerate(downloadContent):
    temp = eachLine.split(',')[0]
    if temp not in priorFiles:
        finalContent.append(temp)

numOfFiles = len(finalContent)

output_file = "to_download_ids.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for content in finalContent:
        out.write(content + "\n")
numOfFilesPerEachWorker = [int(math.floor(float(numOfFiles)/NUMBER_OF_WORKERS)) for x in range(0,NUMBER_OF_WORKERS-1)]
numOfFilesPerEachWorker.append(numOfFiles - (NUMBER_OF_WORKERS-1)*int(round(numOfFiles/NUMBER_OF_WORKERS,0)))

logging.debug("There will be %s workers in this download process" % NUMBER_OF_WORKERS)
logging.debug("%s files will be downloaded" % numOfFiles)

threads = []
imageCount = 0
for i in range(0,NUMBER_OF_WORKERS):
    t = threading.Thread(name='Worker'+str(i), target=worker, args=(finalContent[imageCount:imageCount + numOfFilesPerEachWorker[i]],i,))
    imageCount = imageCount + numOfFilesPerEachWorker[i]
    threads.append(t)
    t.start()

flag = True
while flag:
    counter = 0
    for eachT in threads:
        if not eachT.is_alive():
            counter = counter + 1
    if counter == NUMBER_OF_WORKERS:
        flag = False

logging.debug(str(datetime.datetime.now()) + " - list all files startes ")
allPaths = []
allIDs = []
dirs = os.listdir(os.getcwd())
for eachDir in dirs:
    if 'W' in eachDir:
        FinalList = os.listdir(os.path.join(os.getcwd(),eachDir))
        for eachFile in FinalList:
            if ".jpg" in eachFile:
                fPath = os.path.join(os.getcwd(),eachDir,eachFile)
                fID = eachFile.split(".")[0]
                allPaths.append(fPath)
                allIDs.append(fID)
logging.debug(str(datetime.datetime.now()) + " - write to disc ")

FINAL = codecs.open("FINAL.dat","w","utf-8")
for eachLine in downloadContent:
    tempID = eachLine.split(",")[0]
    try:
        tempIndex = allIDs.index(tempID)
        FINAL.write(eachLine[:-1]+","+str(allPaths[tempIndex])+"\n")
    except:
        FINAL.write(eachLine[:-1]+","+"-\n")
FINAL.close()















                                                                  





