from PIL import Image
from os import listdir, rename
from os.path import isfile, join

IMAGE_FOLDER = "./Images/"
TITLE = "Zenith Finding"
DEFAULT_COLOR = "#ffa700" # d63c18
TITLE_PAGE = "zenithfinding.html"
PAGE_TITLE = "ZF" # format: ZF_CH3_5 for instance
IMAGE_FORMAT = ".png"

CHAPTER_NB = "1" # Can add B after the chapter number bc it's a string

def keep_only_num(string):
    return(int( ''.join(c for c in CHAPTER_NB if c.isdigit()) ))

onlyfiles = [f for f in listdir(IMAGE_FOLDER) if isfile(join(IMAGE_FOLDER, f))]
onlyfiles = sorted(onlyfiles, key=str.lower)

image_path = IMAGE_FOLDER + onlyfiles[0]
img = Image.open(image_path)
width = img.width
height = img.height
half_width = width/2
print(width, height)
img.close()

curr_page = 1
# Getting the names of the pages per chapter
dic_chapters = {} # key = chapter number, value = list of file names
for filename in onlyfiles:
    rename(IMAGE_FOLDER+filename, IMAGE_FOLDER+PAGE_TITLE+"_CH"+CHAPTER_NB+"_"+str(curr_page)+IMAGE_FORMAT)
    chap_num = keep_only_num(CHAPTER_NB)
    if chap_num not in dic_chapters.keys():
        dic_chapters[chap_num] = []
    (dic_chapters[chap_num]).append(filename)
    curr_page += 1

print(dic_chapters)

temp_keys_list = list(dic_chapters.keys())
temp_keys_list.sort()
FIRST_CHAP = -1 # changed my philosophy: now I compile chapter by chapter
LAST_CHAP = keep_only_num(CHAPTER_NB)
NUM_CHAP = len(dic_chapters)

# Writing the html pages
for chap_num, list_pages in dic_chapters.items():
    nb_pages = len(list_pages)
    with open('templatepage.txt', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("$CHAP_NUM", str(chap_num))
    filedata = filedata.replace("$NB_PAGES", str(nb_pages))
    filedata = filedata.replace("$COLOR_CHAP", '"'+DEFAULT_COLOR+'"')
    filedata = filedata.replace("$name_pages", str(list_pages))
    filedata = filedata.replace("$TITLE_PAGE", TITLE_PAGE)
    filedata = filedata.replace("$TITLE", TITLE)
    filedata = filedata.replace("$WIDTH", str(width))
    filedata = filedata.replace("$HEIGHT", str(height))
    filedata = filedata.replace("$HALF_WIDTH", str(half_width))
    filedata = filedata.replace("$FIRST_IMAGE", list_pages[0]) # contains extension .png

    if (chap_num == FIRST_CHAP):
        filedata = filedata.replace("$FIRST_CHAP", "true")
        filedata = filedata.replace("$PREV_CHAP", '""')
    else:
        filedata = filedata.replace("$FIRST_CHAP", "false")
        filedata = filedata.replace("$PREV_CHAP", '"chapter'+str(chap_num-1)+'"') # no chapter skipping
    # if (chap_num == LAST_CHAP):
        # filedata = filedata.replace("$LAST_CHAP", "true")
        # filedata = filedata.replace("$NEXT_CHAP", '""')
    # else:
    filedata = filedata.replace("$LAST_CHAP", "false")
    filedata = filedata.replace("$NEXT_CHAP", '"chapter'+str(chap_num+1)+'"') # no chapter skipping

    list_button_string = ""
    for i in range(0, nb_pages):
        list_button_string += '<button id="button'+str(i)+'" onclick="goToIndex('+str(i)+')">'+str(i+1)+'</button>\n'
    filedata = filedata.replace("$LIST_BUTTON", list_button_string)

    # Write the file out again
    with open('chapter'+str(chap_num)+'.html', 'w') as file:
        file.write(filedata)


# Write the last chapter
with open('templatenextpage.txt', 'r') as file:
    filedata2 = file.read()
filedata2 = filedata2.replace("$TITLE", TITLE)
filedata2 = filedata2.replace("$CHAP_NUM", str(chap_num+1))
with open('chapter'+str(chap_num+1)+'.html', 'w') as file:
    file.write(filedata2)