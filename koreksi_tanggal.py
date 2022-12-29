# -*- coding: utf-8 -*-
"""koreksi_tanggal.ipynb

Automatically generated by Colaboratory.

"""

from sympy import * 
from math import *
import pandas as pd
import calendar
import datetime

def masehi(tahun,lintang,bujur,zona,ketinggian):
  for month1 in range(3,7):

    # inputan yang digunakan
    date_now = datetime.date.today()
    h = date_now.day
    b = month1 #date_now.month
    t = tahun
    ta = int(repr(t)[-2:])
    lin = lintang    
    buj =  bujur   
    zone = zona   
    H = ketinggian      

    # index 30 hari
    dt = datetime.datetime.strptime(f"{h}/{b}/{ta}", "%d/%m/%y")
    form_hari = dt.strftime("%d %b %Y") 
    cal= calendar.Calendar()
    daf_hari = []
    for x in cal.itermonthdays2(t, b):
      if x[0] == 0:
        pass
      else:
        if x[1] == 0:
          daf_hari.append(f'{x[0]:>02d} Sen')
        elif x[1] == 1:
          daf_hari.append(f'{x[0]:>02d} Sel')
        elif x[1] == 2:
          daf_hari.append(f'{x[0]:>02d} Rab')
        elif x[1] == 3:
          daf_hari.append(f'{x[0]:>02d} Kam')
        elif x[1] == 4:
          daf_hari.append(f'{x[0]:>02d} Jum')
        elif x[1] == 5:
          daf_hari.append(f'{x[0]:>02d} Sab')
        else:
          daf_hari.append(f'{x[0]:>02d} Min')

    # display the calendar
    a = calendar.month(t, b).split()
    c = []
    for i in range(9,len(a)):
      c.append(a[i])
    tanggal = list(map(int, c))

    # menghitung jd lokal untuk 1 bulan
    d = []
    for i in tanggal:
      def cek_bulan(b,t):
        if b == 1 or b == 2:
          b = b + 12
          t = t - 1
        else:
          b = b
          t = t
        return b,t

      if t < 0:
        b1,t1 = cek_bulan(b,t)
        A = 0
        B = 0
      else:
        date_1 = datetime.date(t,b,i)
        date_2 = datetime.date(1582,10,4)
        b1,t1 = cek_bulan(b,t)
        if date_1 <= date_2:
          A = 0
          B = 0
        else:
          A = int(t1/100)
          B = 2+int(A/4)-A

      JD = int(365.25*(t1+4716))+int(30.6001*(b1+1))+i+B-1524.5
      jdlokal = JD - zone/24
      d.append(jdlokal)

    # menghitung waktu sholat untuk 1 bulan
    S = []
    TM = []
    D = []
    A = []
    M = []
    I = []
    for i in d:
      #sudut tanggal
      T = 2*pi*(i-2451545)/365.25

      #sudut deklinasi matahari
      delta = degrees(radians(0.37877) + radians(23.264) * sin(radians(57.297*T -79.547)) + radians(0.3812) \
            * sin(radians(2*57.297*T-82.682)) + radians(0.17132) * sin(radians(3*57.297*T-59.722)))

      #bujur rata2 matahari
      def L0(bujur_rata2_matahari):
        while not 0 <= bujur_rata2_matahari <= 360 :
          bujur_rata2_matahari -= 360
        return bujur_rata2_matahari 

      U = (i - 2451545)/36525
      bujur_rata2_matahari = 280.46607 + 36000.7698*U
      L0 = L0(bujur_rata2_matahari)

      #equation of time
      ET = (int(degrees(-radians(1789 + 237 * U) * sin(radians(L0)) - radians(7146 - 62 * U) * cos(radians(L0)) +\
                      radians(9934 - 14 * U) * sin(radians(2 * L0)) - radians(29 + 5 * U) * cos(radians(2 * L0)) + radians(74 + 10*U) *\
                      sin(radians(3 * L0)) + radians(320 - 4 * U) * cos(radians(3 * L0)) - radians(212) * sin(radians(4 * L0)))) + 1) / 1000

      #waktu transit
      waktu_transit = 12 + zone - buj/15 - ET/60


      def convert(waktu_desimal):
        jam = int(waktu_desimal)
        sisa_jam = waktu_desimal - jam
        menit = int(sisa_jam * 60)
        sisa_menit = sisa_jam * 60 - menit
        detik = 60 * sisa_menit
        if detik < 30:
          menit = menit
        else:
          menit = menit + 1

        if menit == 60:
          jam = jam + 1
          menit = 60%60

        if jam >= 24:
          jam = jam%24
        return jam,menit

      def HA(alt):
        hour_angle = degrees(acos((sin(radians(alt)) - sin(radians(lin)) * sin(radians(delta))) / (cos(radians(lin)) * cos(radians(delta)))))
        return hour_angle
      
      #Waktu Subuh
      def subuh():
        try:
          alt = -20
          waktu_subuh = waktu_transit - HA(alt) / 15
        except:
          waktu_subuh = 0
          j,m = convert(waktu_subuh)
        else:
          j,m = convert(waktu_subuh)
        return j,m

      #Waktu Terbit Matahari
      def terbit_matahari():
        try:
          alt = -0.8333 - 0.0347 * sqrt(H)
          waktu_terbit_matahari = waktu_transit - HA(alt) / 15
        except:
          waktu_terbit_matahari = 0
          j,m = convert(waktu_terbit_matahari)
        else:
          j,m = convert(waktu_terbit_matahari)
        return j,m

      #Waktu Dzuhur
      def dzuhur():
        j,m = convert(waktu_transit)
        return j,m

      #Waktu Ashar
      def ashar():
        ka = 1
        alt = degrees(acot(ka + tan(radians(abs(delta - lin)))))
        waktu_ashar = waktu_transit + HA(alt) / 15
        j,m = convert(waktu_ashar)
        return j,m

      #Waktu Maghrib
      def maghrib():
        try:
          alt = -0.8333 - 0.0347 * sqrt(H)
          waktu_maghrib = waktu_transit + HA(alt) / 15
        except:
          waktu_maghrib = 0
          j,m = convert(waktu_maghrib)
        else:
          j,m = convert(waktu_maghrib)
        return j,m

      #Waktu Isya'
      def isya():
        try:
          alt = -18
          waktu_isya = waktu_transit + HA(alt) / 15
        except:
          waktu_isya = 0
          j,m = convert(waktu_isya)
        else:
          j,m = convert(waktu_isya)
        return j,m

      js,ms = subuh()
      jt,mt = terbit_matahari()
      jd,md = dzuhur()
      ja,ma = ashar()
      jm,mm = maghrib()
      ji,mi = isya()

      S.append(f'{js:0>2d}:{ms:0>2d}')
      TM.append(f'{jt:0>2d}:{mt:0>2d}')
      D.append(f'{jd:0>2d}:{md:0>2d}')
      A.append(f'{ja:0>2d}:{ma:0>2d}')
      M.append(f'{jm:0>2d}:{mm:0>2d}')
      I.append(f'{ji:0>2d}:{mi:0>2d}')

    sholat = {f'{dt.strftime("%B")}':daf_hari,
                'Subuh':S,
                'Terbit':TM,
                'Dzuhur':D,
                'Ashar':A,
                'Maghrib':M,
                'Isya':I
                }
    df = pd.DataFrame(sholat).set_index(f'{dt.strftime("%B")}')

    try:
      cari_error_subuh = df["Subuh"].to_list().index('00:00')
      waktu_terakhir_subuh = df["Subuh"].to_list()[cari_error_subuh-1]
    except:
      pass
    else:
      if cari_error_subuh != 0:
        file_bio = open("koreksi_error_subuhM.txt", "w")
        file_bio.write(waktu_terakhir_subuh)
        file_bio.close()
      text_subuh = open('koreksi_error_subuhM.txt','r')
      korektor_subuh = text_subuh.read()
      text_subuh.close()

    try:
      cari_error_isya = df["Isya"].to_list().index('00:00')
      waktu_terakhir_isya = df["Isya"].to_list()[cari_error_isya-1]
    except:
      pass
    else:
      if cari_error_isya != 0:
        file_bio = open("koreksi_error_isyaM.txt", "w")
        file_bio.write(waktu_terakhir_isya)
        file_bio.close()
      text_isya = open('koreksi_error_isyaM.txt','r')
      korektor_isya = text_isya.read()
      text_isya.close()

    try:
      cari_error_terbit = df["Terbit"].to_list().index('00:00')
      waktu_terakhir_terbit = df["Terbit"].to_list()[cari_error_terbit-1]
    except:
      pass
    else:
      if cari_error_terbit != 0:
        file_bio = open("koreksi_error_terbitM.txt", "w")
        file_bio.write(waktu_terakhir_terbit)
        file_bio.close()
      text_terbit = open('koreksi_error_terbitM.txt','r')
      korektor_terbit = text_terbit.read()
      text_terbit.close()

    try:
      cari_error_maghrib = df["Maghrib"].to_list().index('00:00')
      waktu_terakhir_maghrib = df["Maghrib"].to_list()[cari_error_maghrib-1]
    except:
      pass
    else:
      if cari_error_maghrib != 0:
        file_bio = open("koreksi_error_maghribM.txt", "w")
        file_bio.write(waktu_terakhir_maghrib)
        file_bio.close()
      text_maghrib = open('koreksi_error_maghribM.txt','r')
      korektor_maghrib = text_maghrib.read()
      text_maghrib.close()
  return korektor_subuh,korektor_terbit,korektor_maghrib,korektor_isya

from math import *
from sympy import *
import hijri_converter.convert
import pandas as pd

def hijriyah(tahun,lintang,bujur,zona,ketinggian):
  for month1 in range (9,12):
    hijri_now = hijri_converter.Hijri.today()
    h = hijri_now.day
    b = month1
    t = tahun
    total_hari_hijriyah = hijri_converter.Hijri(t,b,h).month_length()
    lin = lintang
    buj =  bujur   
    zone = zona
    H = ketinggian     

    c = []
    for i in range(1, total_hari_hijriyah + 1):
      gregorian = hijri_converter.Hijri(t,b,i).to_gregorian()
      #tanggal = gregorian.strptime(gregorian,)
      masehi = gregorian.strftime('%d %b %Y')
      c.append(f'{i:0>2d} ({masehi})')

    list_jd_hijriyah = []
    for i in range(1, total_hari_hijriyah + 1):
      #tahun yang sudah dilewati
      t1 = int((t - 1)/30)
      ts = ((t - 1)%30)

      if ts<2:
        k = 0
      elif 2<=ts<5:
        k = 1
      elif 5<=ts<7:
        k = 2
      elif 7<=ts<10:
        k = 3
      elif 10<=ts<13:
        k = 4
      elif 13<=ts<16:
        k = 5
      elif 16<=ts<18:
        k = 6
      elif 18<=ts<21:
        k = 7
      elif 21<=ts<24:
        k = 8
      elif 24<=ts<26:
        k = 9
      elif 26<=ts<29:
        k = 10
      else:
        k = 11

      #jumlah hari yang sudah dilewati
      hariDilewati = (t1*((354*30) + 11)) + ((ts*354) + k)

      #jumlah hari dalam tahun yang berjalan
      list_hariBerjalan = [0,30,59,89,118,148,177,207,236,266,295,325,354]
      b1 = b - 1

      for berjalan,hari in enumerate(list_hariBerjalan):
        if berjalan == b1:
          hariBerjalan = hari

      hariTahunIni = hariBerjalan + i
      #hijriah ke julian day
      JD = 1948438.5 + hariDilewati + hariTahunIni
      jdlokal = JD - zone/24
      list_jd_hijriyah.append(jdlokal)

    S = []
    TM = []
    D = []
    A = []
    M = []
    I = []
    for jd in list_jd_hijriyah:
      #sudut tanggal
      T = 2*pi*(jd-2451545)/365.25

      #sudut deklinasi matahari
      delta = degrees(radians(0.37877) + radians(23.264) * sin(radians(57.297*T -79.547)) + radians(0.3812) \
            * sin(radians(2*57.297*T-82.682)) + radians(0.17132) * sin(radians(3*57.297*T-59.722)))

      #bujur rata2 matahari
      def L0(bujur_rata2_matahari):
        while not 0 <= bujur_rata2_matahari <= 360 :
          bujur_rata2_matahari -= 360
        return bujur_rata2_matahari 

      U = (jd - 2451545)/36525
      bujur_rata2_matahari = 280.46607 + 36000.7698*U
      L0 = L0(bujur_rata2_matahari)

      #equation of time
      ET = (int(degrees(-radians(1789 + 237 * U) * sin(radians(L0)) - radians(7146 - 62 * U) * cos(radians(L0)) +\
                      radians(9934 - 14 * U) * sin(radians(2 * L0)) - radians(29 + 5 * U) * cos(radians(2 * L0)) + radians(74 + 10*U) *\
                      sin(radians(3 * L0)) + radians(320 - 4 * U) * cos(radians(3 * L0)) - radians(212) * sin(radians(4 * L0)))) + 1) / 1000

      #waktu transit
      waktu_transit = 12 + zone - buj/15 - ET/60


      def convert(waktu_desimal):
        jam = int(waktu_desimal)
        sisa_jam = waktu_desimal - jam
        menit = int(sisa_jam * 60)
        sisa_menit = sisa_jam * 60 - menit
        detik = 60 * sisa_menit
        if detik < 30:
          menit = menit
        else:
          menit = menit + 1

        if menit == 60:
          jam = jam + 1
          menit = 60%60

        if jam >= 24:
          jam = jam%24
        return jam,menit

      def HA(alt):
        hour_angle = degrees(acos((sin(radians(alt)) - sin(radians(lin)) * sin(radians(delta))) / (cos(radians(lin)) * cos(radians(delta)))))
        return hour_angle

      #Waktu Subuh
      def subuh():
        try:
          alt = -20
          waktu_subuh = waktu_transit - HA(alt) / 15
        except:
          waktu_subuh = 0
          j,m = convert(waktu_subuh)
        else:
          j,m = convert(waktu_subuh)
        return j,m

      #Waktu Terbit Matahari
      def terbit_matahari():
        try:
          alt = -0.8333 - 0.0347 * sqrt(H)
          waktu_terbit_matahari = waktu_transit - HA(alt) / 15
        except:
          waktu_terbit_matahari = 0
          j,m = convert(waktu_terbit_matahari)
        else:
          j,m = convert(waktu_terbit_matahari)
        return j,m

      #Waktu Dzuhur
      def dzuhur():
        j,m = convert(waktu_transit)
        return j,m

      #Waktu Ashar
      def ashar():
        ka = 1
        alt = degrees(acot(ka + tan(radians(abs(delta - lin)))))
        waktu_ashar = waktu_transit + HA(alt) / 15
        j,m = convert(waktu_ashar)
        return j,m

      #Waktu Maghrib
      def maghrib():
        try:
          alt = -0.8333 - 0.0347 * sqrt(H)
          waktu_maghrib = waktu_transit + HA(alt) / 15
        except:
          waktu_maghrib = 0
          j,m = convert(waktu_maghrib)
        else:
          j,m = convert(waktu_maghrib)
        return j,m

      #Waktu Isya'
      def isya():
        try:
          alt = -18
          waktu_isya = waktu_transit + HA(alt) / 15
        except:
          waktu_isya = 0
          j,m = convert(waktu_isya)
        else:
          j,m = convert(waktu_isya)
        return j,m

      js,ms = subuh()
      jt,mt = terbit_matahari()
      jd,md = dzuhur()
      ja,ma = ashar()
      jm,mm = maghrib()
      ji,mi = isya()

      S.append(f'{js:0>2d}:{ms:0>2d}')
      TM.append(f'{jt:0>2d}:{mt:0>2d}')
      D.append(f'{jd:0>2d}:{md:0>2d}')
      A.append(f'{ja:0>2d}:{ma:0>2d}')
      M.append(f'{jm:0>2d}:{mm:0>2d}')
      I.append(f'{ji:0>2d}:{mi:0>2d}')  

    sholat_hijriyah = {
        f'{hijri_now.month_name()}':c,
        'Subuh'  : S,
        'Terbit' : TM,
        'Dzuhur' : D,
        'Ashar'  : A,
        'Maghrib': M,
        'Isya'   : I
    }
    df = pd.DataFrame(sholat_hijriyah).set_index(f'{hijri_now.month_name()}')

    try:
      cari_error_subuh = df["Subuh"].to_list().index('00:00')
      waktu_terakhir_subuh = df["Subuh"].to_list()[cari_error_subuh-1]
    except:
      pass
    else:
      if cari_error_subuh != 0:
        file_bio = open("koreksi_error_subuhH.txt", "w")
        file_bio.write(waktu_terakhir_subuh)
        file_bio.close()
      text_subuh = open('koreksi_error_subuhH.txt','r')
      korektor_subuh = text_subuh.read()
      text_subuh.close()

    try:
      cari_error_isya = df["Isya"].to_list().index('00:00')
      waktu_terakhir_isya = df["Isya"].to_list()[cari_error_isya-1]
    except:
      pass
    else:
      if cari_error_isya != 0:
        file_bio = open("koreksi_error_isyaH.txt", "w")
        file_bio.write(waktu_terakhir_isya)
        file_bio.close()
      text_isya = open('koreksi_error_isyaH.txt','r')
      korektor_isya = text_isya.read()
      text_isya.close()

    try:
      cari_error_terbit = df["Terbit"].to_list().index('00:00')
      waktu_terakhir_terbit = df["Terbit"].to_list()[cari_error_terbit-1]
    except:
      pass
    else:
      if cari_error_terbit != 0:
        file_bio = open("koreksi_error_terbitH.txt", "w")
        file_bio.write(waktu_terakhir_terbit)
        file_bio.close()
      text_terbit = open('koreksi_error_terbitH.txt','r')
      korektor_terbit = text_terbit.read()
      text_terbit.close()

    try:
      cari_error_maghrib = df["Maghrib"].to_list().index('00:00')
      waktu_terakhir_maghrib = df["Maghrib"].to_list()[cari_error_maghrib-1]
    except:
      pass
    else:
      if cari_error_maghrib != 0:
        file_bio = open("koreksi_error_maghribH.txt", "w")
        file_bio.write(waktu_terakhir_maghrib)
        file_bio.close()
      text_maghrib = open('koreksi_error_maghribH.txt','r')
      korektor_maghrib = text_maghrib.read()
      text_maghrib.close()
  return korektor_subuh,korektor_terbit,korektor_maghrib,korektor_isya
