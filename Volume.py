#                     LEVEL 1 - UPLOADING A FILE


# UPLOADING COORDINATES OF EXTERNAL CONTOUR
# uploading coordinates from file (wsp low.txt)
with open ('wsp low.txt', 'r') as file:
    wsp_low = file.readlines()

wsp_low2=[]
for i in wsp_low:
    wsp_low2.append(i.replace('\n', ''))

# separating coordinates into a list
wsp_low3 = []
for i in wsp_low2:
    wsp_low3.append(i.split())


# UPLOADING COORDINATES OF MEASURED POINTS  (WITHOUT EXTERNAL CONTOUR)
# uploading coordinates from file (wsp high.txt)
with open ('wsp high.txt', 'r') as file:
    wsp_high = file.readlines()

wsp_high2=[]
for i in wsp_high:
    wsp_high2.append(i.replace('\n', ''))

# separating coordinates into a list
wsp_high3 = []
for i in wsp_high2:
    wsp_high3.append(i.split())


del(wsp_high)
del(wsp_high2)
del(wsp_low)
del(wsp_low2)

# END OF STAGE 1 - RESULT: UPLOADING 2 FILES:
# wsp_low3 - COORDINATES OF EXTERNAL CONTOUR
# wsp_high3 - UPLOADING COORDINATES OF MEASURED POINTS

