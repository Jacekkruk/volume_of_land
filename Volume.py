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


def is_point_belong_outline(min_d, wsp_low3):
    outline = False
    for point in wsp_low3:
        if point[0] == min_d[2]:
            outline = True
            print('Uwaga punkt z obrysu- obrys = true')
            return outline
    if outline == False:
        return outline


def is_point_inside_is_correcty(Azymut_A_min_d, Azymut_A_wsp_pktB, Azymut_A_wsp_pktC):
    if Azymut_A_wsp_pktC > Azymut_A_wsp_pktB:
        # assumption nr 1: Azimuth AC greater then AB
        if (math.radians(360) - Azymut_A_wsp_pktC + Azymut_A_wsp_pktB) > math.radians(
                180):  # assumption that angle greater then 200g
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
        else:  # assumption when trinagle less then 200g:
            if 0 < Azymut_A_min_d < Azymut_A_wsp_pktB or Azymut_A_wsp_pktC <= Azymut_A_min_d < math.radians(360):
                punkt = True
            else:
                punkt = False
    else:
        # Assumption nr 2: Azimuth AC less then AB
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









