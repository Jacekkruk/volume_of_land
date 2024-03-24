#                     LEVEL 1 - UPLOADING A FILE
import math

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

wsp_low_for_high = wsp_low3.copy()  #  copy of coordinates external contour
                                    # to determine the height of the reference level points


# FUNCTIONS DEFINITIONS

def azymutA_B(Xa, Ya, Xb, Yb):  # Coordinates x in mathematical system (approx  x = 7500000 y = 5800000)
    if Xa == Xb and Ya < Yb:
        Azymut_A_B = 0
    elif Xa == Xb and Ya > Yb:
        Azymut_A_B = math.radians(180)
    elif Ya == Yb and Xa < Xb:
        Azymut_A_B = math.radians(90)
    elif Ya == Yb and Xa > Xb:
        Azymut_A_B = math.radians(270)
    else:

        if (float(Xb) - float(Xa)) > 0 and (float(Yb) - float(Ya)) > 0:
            Azymut_A_B = math.atan((float(Xb) - float(Xa)) / (float(Yb) - float(Ya)))

        elif (float(Xb) - float(Xa)) > 0 and (float(Yb) - float(Ya)) < 0:
            Azymut_A_B = math.atan((float(Xb) - float(Xa)) / (float(Yb) - float(Ya))) + math.radians(180)

        elif (float(Xb) - float(Xa)) < 0 and (float(Yb) - float(Ya)) < 0:
            Azymut_A_B = math.atan((float(Xb) - float(Xa)) / (float(Yb) - float(Ya))) + math.radians(180)

        elif (float(Xb) - float(Xa)) < 0 and (float(Yb) - float(Ya)) > 0:
            Azymut_A_B = math.atan((float(Xb) - float(Xa)) / (float(Yb) - float(Ya))) + math.radians(360)
    return Azymut_A_B


def Czy_punkt_nalezy_do_obrysu(min_d, wsp_low3):
    obrys = False
    for point in wsp_low3:
        if point[0] == min_d[2]:
            obrys = True
            print('Uwaga punkt z obrysu- obrys = true')
            return obrys
    if obrys == False:
        return obrys


def spradzenie_czy_punkt_wewnatrz_poprawny(Azymut_A_min_d, Azymut_A_wsp_pktB, Azymut_A_wsp_pktC):
    if Azymut_A_wsp_pktC > Azymut_A_wsp_pktB:
        # Założenie nr 1: Azymut AC większy AB
        if (math.radians(360) - Azymut_A_wsp_pktC + Azymut_A_wsp_pktB) > math.radians(
                180):  # założenie ze kąt wiekszy niż 200g
            if Azymut_A_wsp_pktB > math.radians(180) and Azymut_A_min_d > Azymut_A_wsp_pktB - math.radians(
                    180) and Azymut_A_min_d < Azymut_A_wsp_pktB:

                punkt = True
            elif Azymut_A_wsp_pktB < math.radians(180):
                if Azymut_A_min_d < Azymut_A_wsp_pktB or math.radians(
                        360) > Azymut_A_min_d > Azymut_A_wsp_pktB + math.radians(180):
                    punkt = True
                else:
                    punkt = False
            else:
                punkt = False
        else:  # założenia gdy kąt jest mniejszy niż 200g:
            if 0 < Azymut_A_min_d < Azymut_A_wsp_pktB or Azymut_A_wsp_pktC <= Azymut_A_min_d < math.radians(360):
                punkt = True
            else:
                punkt = False
    else:
        # Założenie nr 2: Azymut AC mniejszy AB
        if (Azymut_A_wsp_pktB - Azymut_A_wsp_pktC) > math.radians(180):
            if Azymut_A_wsp_pktB - math.radians(180) < Azymut_A_min_d < Azymut_A_wsp_pktB:
                punkt = True
            else:
                punkt = False
        else:
            if Azymut_A_wsp_pktC <= Azymut_A_min_d < Azymut_A_wsp_pktB:
                punkt = True
            else:
                punkt = False
    return punkt


def if_point_inside_triangle(x1, y1, x2, y2, x3, y3, xp, yp):
    c1 = (x2 - x1) * (yp - y1) - (y2 - y1) * (xp - x1)
    c2 = (x3 - x2) * (yp - y2) - (y3 - y2) * (xp - x2)
    c3 = (x1 - x3) * (yp - y3) - (y1 - y3) * (xp - x3)
    if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
        print("The point is in the triangle.")
        return True
    else:
        return False




# ETAP 2 - CHECKING THE DIRECTION EXTERNAL CONTOUR


# checking the direction external contour. Count right triangle
    # (1) Count right triangle for first point
    # (2) Count right triangle for last point
    # (3) Count right triangle for intermediate points


suma_kat = 0

for n, pkt in enumerate(wsp_low3):

    # (1) Count right triangle for first point
    #   Azimuth to next point
    if n == 0:

        Azymut_A_B = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[n + 1][2], wsp_low3[n + 1][1])

        #   Azimuth to previous point
        Azymut_A_Z = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[-1][2], wsp_low3[-1][1])

        # Count right triangle for n =0
        if (Azymut_A_Z - Azymut_A_B) > 0:
            delta_Azymut = Azymut_A_Z - Azymut_A_B
        else:
            delta_Azymut = 2 * math.pi - Azymut_A_B + Azymut_A_Z
        suma_kat += delta_Azymut


    # (2) Count right triangle for last point
    # Azimuth to next point (that is first)
    elif n == (len(wsp_low3) - 1):

        Azymut_A_B = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[0][2], wsp_low3[0][1])

        # Azimuth to next point (that is penultimate - second last)

        Azymut_A_Z = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[n - 1][2], wsp_low3[n - 1][1])

        # Count right triangle for n  - last

        if (Azymut_A_Z - Azymut_A_B) > 0:
            delta_Azymut = Azymut_A_Z - Azymut_A_B
        else:
            delta_Azymut = 2 * math.pi - Azymut_A_B + Azymut_A_Z
        suma_kat += delta_Azymut

    else:
        # (3) Count right triangle for intermediate points
        # Azimuth to next point (that is  n+1)

        Azymut_A_B = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[n + 1][2], wsp_low3[n + 1][1])

        # Azimuth to previous point (that is  n-1)

        Azymut_A_Z = azymutA_B(wsp_low3[n][2], wsp_low3[n][1], wsp_low3[n - 1][2], wsp_low3[n - 1][1])

        # Count right triangle for n intermediate

        if (Azymut_A_Z - Azymut_A_B) > 0:
            delta_Azymut = Azymut_A_Z - Azymut_A_B
        else:
            delta_Azymut = 2 * math.pi - Azymut_A_B + Azymut_A_Z
        suma_kat += delta_Azymut

# CHECKING THE DIRECTION EXTERNAL CONTOUR
# direction = 1 - right direction
# direction = 0 - left direction

if round(suma_kat, 5) == round((len(wsp_low3) - 2) * math.pi, 5):
    direction = 1
elif round(suma_kat, 5) == round(2 * math.pi * len(wsp_low3) - math.pi * (len(wsp_low3) - 2), 5):
    direction = 0
else:
    direction = -1

# print direction
if direction == 1:
    print('Right direction')
elif direction == 0:
    print('Left direction')
else:
    print('Something is wrong - check direction !!!')

# change direction to the right if it was left

if direction == 0:
    wsp_low3 = wsp_low3[::-1]
    print('Direction has been changed to right')

# END OF STAGE 2

triangle = False
licznik_punktów_w_trojkacie = 0
triangle_list = []  # triangle list


# START MAIN LOOP

punkt = True
obrys = False
obrys_czy_punkt_nastepny = True
obrys_czy_punkt_poprzedni = False

# Creating first variables
wsp_pktA = wsp_low3[0]
wsp_pktB = wsp_low3[-1]
wsp_pktC = wsp_low3[1]

copywsp_low3 = wsp_low3.copy()
copywsp_high3 = wsp_high3.copy()
copywsp_low3.remove(wsp_pktA)
copywsp_low3.remove(wsp_pktB)

# ETAP 3 - CREATING NET LEAST TRIANGLE

numer_petli = 1

while len(wsp_low3) > 3:

    # additional assumption where we have points but it cant find triangle
    if len(copywsp_low3) == 1 and len(wsp_low3) > 3:
        wsp_low3.append(wsp_low3[0])
        wsp_low3.pop(0)
        print('no triangle found, so we move the outline further')

        wsp_pktA = wsp_low3[0]
        wsp_pktB = wsp_low3[-1]
        wsp_pktC = wsp_low3[1]

        copywsp_low3 = wsp_low3.copy()
        copywsp_high3 = wsp_high3.copy()
        copywsp_low3.remove(wsp_pktA)
        copywsp_low3.remove(wsp_pktB)

    print('\nNUMBER OF LOOP', numer_petli)
    numer_petli += 1

    #                STAGE 3A - DETERMINING THE SHORTEST DISTANCE
    # point A the first point in EXTERNAL CONTOUR
    # point B the last point in EXTERNAL CONTOUR
    # point C second point in EXTERNAL CONTOUR

    if punkt == True and obrys == False and triangle == False:
        wsp_pktA = wsp_low3[0]
        wsp_pktB = wsp_low3[-1]
        wsp_pktC = wsp_low3[1]

        copywsp_low3 = wsp_low3.copy()
        copywsp_high3 = wsp_high3.copy()
        copywsp_low3.remove(wsp_pktA)
        copywsp_low3.remove(wsp_pktB)

    if punkt == True and obrys == True and obrys_czy_punkt_nastepny == True and triangle == False:
        wsp_pktA = wsp_low3[0]
        wsp_pktB = wsp_low3[-1]
        wsp_pktC = wsp_low3[1]

        copywsp_low3 = wsp_low3.copy()
        copywsp_high3 = wsp_high3.copy()
        copywsp_low3.remove(wsp_pktA)
        copywsp_low3.remove(wsp_pktB)

    if punkt == True and obrys == True and obrys_czy_punkt_poprzedni == True and triangle == False:
        wsp_pktA = wsp_low3[0]
        wsp_pktB = wsp_low3[-1]
        wsp_pktC = wsp_low3[1]

        copywsp_low3 = wsp_low3.copy()
        copywsp_high3 = wsp_high3.copy()
        copywsp_low3.remove(wsp_pktA)
        copywsp_low3.remove(wsp_pktB)

    if triangle == True:
        wsp_low3.append(wsp_low3[0])
        wsp_low3.pop(0)
        print('in previous loop triangle = True so we move next ')

        wsp_pktA = wsp_low3[0]
        wsp_pktB = wsp_low3[-1]
        wsp_pktC = wsp_low3[1]

        copywsp_low3 = wsp_low3.copy()
        copywsp_high3 = wsp_high3.copy()
        copywsp_low3.remove(wsp_pktA)
        copywsp_low3.remove(wsp_pktB)

    triangle = False
    obrys_czy_punkt_nastepny = False

    # destince calculation from point A to points in external contour (without point B)

    dist_fromA = []
    dist_fromB = []
    wsp_ALL = copywsp_low3 + copywsp_high3
    wsp_ALL_Baza = wsp_low3 + wsp_high3

    for num, i in enumerate(wsp_ALL):
        di = ((float(i[1]) - float(wsp_pktA[1])) ** 2 + (float(i[2]) - float(wsp_pktA[2])) ** 2) ** (1 / 2)
        dist_fromA.append([num, di])

    # destince calculation from point B to points in external contour (without point A)

    for num, i in enumerate(wsp_ALL):
        di = ((float(i[1]) - float(wsp_pktB[1])) ** 2 + (float(i[2]) - float(wsp_pktB[2])) ** 2) ** (1 / 2)
        dist_fromB.append([num, di])

        # Determining the minimum sum of distances (min_d variable)
    sum_all = []
    for i, j in dist_fromA:
        sum = j + dist_fromB[i][1]
        sum_all.append([i, sum])
    sum_all.sort(key=lambda i: i[1])

    min_d = sum_all[0] + wsp_ALL[sum_all[0][0]]
    print(min_d)



    #               STEGE 3B - ASSUMPTIONS FOR THE POINT FOUND

    # Checking whether a given point belongs to the earth embankment

    # 3B.1 Checking whether the selected point is within the external contour :

    obrys = Czy_punkt_nalezy_do_obrysu(min_d, wsp_low3)

    if obrys == True:  # if point in external contour we check if point is correct

        # Azimuth calculation:

        # Azimuth calculation from point A to point min_d
        Azymut_A_min_d = azymutA_B(wsp_pktA[2], wsp_pktA[1], min_d[4], min_d[3])

        # Azimuth calculation from point A to privous point B: wsp_pktB
        Azymut_A_wsp_pktB = azymutA_B(wsp_pktA[2], wsp_pktA[1], wsp_pktB[2], wsp_pktB[1])

        # Azimuth calculation from point A to next point C: wsp_pktC
        Azymut_A_wsp_pktC = azymutA_B(wsp_pktA[2], wsp_pktA[1], wsp_pktC[2], wsp_pktC[1])

        # 4.1.1 Assumption for point min_d for externel contour
        # poin = False incorrect point
        # poin = True correct point

        punkt = spradzenie_czy_punkt_wewnatrz_poprawny(Azymut_A_min_d, Azymut_A_wsp_pktB, Azymut_A_wsp_pktC)

        if punkt == True:

            # checking whether there is a point in the triangle
            for i in wsp_ALL_Baza:
                triangle = if_point_inside_triangle(float(wsp_pktA[2]), float(wsp_pktA[1]), float(wsp_pktB[2]),
                                                    float(wsp_pktB[1]), float(min_d[4]), float(min_d[3]), float(i[2]),
                                                    float(i[1]))
                if i == min_d:
                    continue
                elif triangle == True:
                    print('ERROR point', i[0])
                    licznik_punktów_w_trojkacie += 1
                    break

            if min_d[2] == wsp_pktC[0] and triangle == False:
                triangle_list.append([min_d[2:], wsp_pktA, wsp_pktB])
                wsp_low3.pop(0)
                obrys_czy_punkt_nastepny = True
                obrys_czy_punkt_poprzedni = False

            elif min_d[2] == wsp_low3[-2][0] and triangle == False:
                triangle_list.append([min_d[2:], wsp_pktA, wsp_pktB])
                print('new asumption works')
                wsp_low3.pop(-1)
                obrys_czy_punkt_poprzedni = True
                obrys_czy_punkt_nastepny = False

            else:
                if triangle == False:

                    obrys_czy_punkt_nastepny = False
                    obrys_czy_punkt_poprzedni = False
                    for i, j in enumerate(copywsp_low3):
                        if j[0] == min_d[2]:
                            print('usunięto punkt z bazy dolnej', copywsp_low3[i])
                            copywsp_low3.pop(i)



        else:  # if point = false - so it is incorrect point - delete point from bazy dolnej copy
            for i, j in enumerate(copywsp_low3):
                if j[0] == min_d[2]:
                    copywsp_low3.pop(i)



    else:
        # Point is inside so we keep checking

        # 3B.2 AZIMUTH CALCULATING:
        # Azimuth calculating from point A to point min_d
        Azymut_A_min_d = azymutA_B(wsp_pktA[2], wsp_pktA[1], min_d[4], min_d[3])

        # Azimuth calculating from point A to prvious point B: wsp_pktB
        Azymut_A_wsp_pktB = azymutA_B(wsp_pktA[2], wsp_pktA[1], wsp_pktB[2], wsp_pktB[1])

        # Azimuth calculating from point A to next point C: wsp_pktC
        Azymut_A_wsp_pktC = azymutA_B(wsp_pktA[2], wsp_pktA[1], wsp_pktC[2], wsp_pktC[1])

        # 4.3 assumption for point min_d:
        # point = False incorrect point
        # point = True correct point

        punkt = spradzenie_czy_punkt_wewnatrz_poprawny(Azymut_A_min_d, Azymut_A_wsp_pktB, Azymut_A_wsp_pktC)

    if punkt == True and obrys == False and triangle == False:
        triangle_list.append([min_d[2:], wsp_pktA, wsp_pktB])
        # add point to 'wsp high.txt' and delete it from external contour
        wsp_low3.append(min_d[2:])

        for i, j in enumerate(wsp_high3):
            if j[0] == min_d[2]:
                wsp_high3.pop(i)
    elif punkt == False and obrys == False and triangle == False:
        for i, j in enumerate(copywsp_high3):
            if j[0] == min_d[2]:
                copywsp_high3.pop(i)
    elif punkt == True and obrys == True and obrys_czy_punkt_nastepny == False and obrys_czy_punkt_poprzedni == False and triangle == False:
        # point is in contour and meets the assumptions but it is next point in previous so we
        # delete it from base copywsp_low3 and go on
        for i, j in enumerate(copywsp_low3):
            if j[0] == min_d[2]:
                copywsp_low3.pop(i)

if len(wsp_low3) == 3:
    triangle_list.append([wsp_low3[0], wsp_low3[1], wsp_low3[2]])

# END STAGE 3 - WE HAVE TRIANGLES

# STAGE 4 IMPORT TO AUTOCAD NET TRIANGLE
# REMMEMBER: Autocad file must be in folder and it must be open

from pyautocad import (Autocad, APoint)
acad = Autocad(create_if_not_exists=True)

for trian in triangle_list:
# triangles point
    punkt_1 = APoint(float(trian[0][2]), float(trian[0][1]), float(trian[0][3]))
    punkt_2 = APoint(float(trian[1][2]), float(trian[1][1]), float(trian[1][3]))
    punkt_3 = APoint(float(trian[2][2]), float(trian[2][1]), float(trian[2][3]))
    acad.model.AddLine(punkt_1, punkt_2)
    acad.model.AddLine(punkt_1, punkt_3)
    acad.model.AddLine(punkt_2, punkt_3)
acad.app.ZoomExtents()
#    acad.model.AddPoint(punkt_1)

#                            STAGE 5 CALCULATION OF HEIGHT POINTS

'''We calculate the height of a point by calculating the distance to each point from external contour,
   the longest distance has a weight of 1, while the weights of the remaining points are
   the quotient of the longest distance and the distance to a given next point on the contour
'''

def spr_czy_pkt_nalezy_do_obrysu(punkt):
    flag = False
    for i in wsp_low_for_high:
        if i[0] == punkt[0]:
            flag = True
            break
    if flag == True:
        return True  # if point from contour
    else:
        return False  # if point from inside


# calculation list with added variable - is_point_contour(TRUE) is_point_inside(FALSE)


triangle_list_with_true_false = list(
    map(lambda x: [[x[0][0], x[0][1], x[0][2], x[0][3], spr_czy_pkt_nalezy_do_obrysu(x[0])],
                   [x[1][0], x[1][1], x[1][2], x[1][3], spr_czy_pkt_nalezy_do_obrysu(x[1])],
                   [x[2][0], x[2][1], x[2][2], x[2][3], spr_czy_pkt_nalezy_do_obrysu(x[2])]],
        triangle_list))


# calculation list with added variable - height references in given point
def obl_reference_level(punkt):

    high = punkt[4]
    if high == True:
        return punkt[3]
    else:
        distances = list(map(lambda x: [x[0], (
                    (float(x[1]) - float(punkt[1])) ** 2 + (float(x[2]) - float(punkt[2])) ** 2) ** (
                                                    1 / 2), x[3]], wsp_low_for_high))
        dist_maximum = 0
        for i in distances:
            if i[1] > dist_maximum:
                dist_maximum = i[1]

        distances_waga = list(map(lambda x: [x[0], x[1], x[2], dist_maximum / x[1]], distances))

        suma_iloczynow = 0
        suma_wag = 0
        for i in distances_waga:
            suma_iloczynow += float(i[2]) * i[3]
            suma_wag += i[3]
        return suma_iloczynow / suma_wag


# List of triangles with height and references height in given point

triangle_list_with_reference_level = list(
    map(lambda x: [[x[0][0], x[0][1], x[0][2], x[0][3], obl_reference_level(x[0])],
                   [x[1][0], x[1][1], x[1][2], x[1][3], obl_reference_level(x[1])],
                   [x[2][0], x[2][1], x[2][2], x[2][3], obl_reference_level(x[2])]],
        triangle_list_with_true_false))

# END STAGE 5


#                            STEGE 6 calculating the area of a triangle

# We use the formula for the area of a triangle
# P 1/2 |(Xb-Xa)(Yc-Ya)-(Xc-Xa)(Yb-Ya)|

def area(xa, ya, xb, yb, xc, yc):
    area = abs(((xb - xa) * (yc - ya) - (xc - xa) * (yb - ya)) / 2)
    return area


# List of triangles with height and references height in given point and area
# point [point A, X, Y, Z, Z_reference],[point B, X, Y, Z, Z_reference],
#                                        [point C, X, Y, Z, Z_reference], Area)

triangle_list_with_reference_level_and_area = []

for i in triangle_list_with_reference_level:
    i.append(area(float(i[0][1]), float(i[0][2]),
                  float(i[1][1]), float(i[1][2]),
                  float(i[2][1]), float(i[2][2])))
    triangle_list_with_reference_level_and_area.append(i)

#                            STAGE 7 Calculate volume of triangles

triangle_list_with_reference_level_area_and_volume = []

for i in triangle_list_with_reference_level_and_area:
    avarage_z = (float(i[0][3]) + float(i[1][3]) + float(i[2][3])) / 3
    avarage_references_level = (float(i[0][4]) + float(i[1][4]) + float(i[2][4])) / 3
    delta_z = avarage_z - avarage_references_level
    volume = delta_z * i[3]
    i.append(volume)
    triangle_list_with_reference_level_area_and_volume.append(i)

#                            STAGE 8 Sum of volume

volume = 0

for i in triangle_list_with_reference_level_area_and_volume:
    volume += i[4]

print(30 * '*')
print(' Finish volume :', round(volume,2))






