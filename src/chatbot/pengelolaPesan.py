import chatbot.booyer as booyer
import chatbot.models as models
import re
import datetime
def olahPesan(pesan):
    daftarKosakata = models.DaftarKata.objects.all()
    #print(daftarKosakata[0].kosakata)
    if(checkIsNewTask(pesan,daftarKosakata)):
        return newTask(pesan,daftarKosakata)
    elif(checkIsTaskChecker(pesan)):
        return taskChecker(pesan,daftarKosakata)
    elif(checkIsDeadlineChekcer(pesan,daftarKosakata)):
        return deadlineChecker(pesan,daftarKosakata)
    elif(checkIsRenewTask(pesan)):
        return renewTask(pesan)
    elif(checkIsMarkTask(pesan)):
        return markTask(pesan)
    elif(checkIsHelp(pesan)):
        return getHelp(daftarKosakata)
    else:
        return {
            "status" : "ok",
            "header" : "Not found",
            "pesan"  : [
                "Maaf, pesan tidak dikenali",
                autoFixMessage(pesan)
            ]
        }

def checkIsHelp(pesan : str):
    pesan = pesan.lower()
    c1 = re.match(r'[a-z ]+dapat[ ]+[a-z ]+lakukan',pesan)
    c2 = re.match(r'[a-z ]+bisa[ ]+[a-z ]+lakukan',pesan)
    c3 = re.match(r'bantu*[ain]',pesan)
    return c1 or c2 or c3

def getHelp(listKosakata):
    temp = {
        "status": "ok",
        "header": "Informasi Bot",
        "pesan": [
            "[Fitur]",
            "1. Menambahkan task baru",
            "2. Memperbarui deadlinetask",
            "3. Melihat daftar task",
            "4. Menandai task yang sudah selesai",
            "5. Menampilkan bantuan",
            "6. Menampilkan deadline sesuai filter",
            "[Daftar Kata Penting]",
        ]
    }
    for i in range(len(listKosakata)):
        temp["pesan"].append(str(i+1)+". "+str(listKosakata[i].kosakata))
    return temp

def checkIsNewTask(pesan,listKosakata):
    re_matkul = '(if|ii|ku|ti|ma|fi|el)[1-5][0-9][0-9][0-9]'
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'
    re_waktu3 = '((besok|lusa)|((minggu|bulan)[ ]depan))'
    pesan = pesan.lower()
    kodematkul = re.match(".*"+re_matkul,pesan)
    waktu = re.match("[0-9a-z ]*" + re_waktu1, pesan) or re.match("[0-9a-z ]*" + re_waktu2, pesan) or re.match(".*" + re_waktu3, pesan)
    for x in listKosakata:
        kosakata = re.match('.*'+x.kosakata,pesan)
        topik = len(re.findall(re_matkul + "\s",pesan))>0 or len(re.findall(x.kosakata + "\s",pesan))>0
        if kosakata: break

    return topik and kodematkul and kosakata and waktu

def newTask(pesan,listKosakata):
    re_matkul = r'(if|ii|ku|ti|ma|fi|el)[1-5][0-9][0-9][0-9]'
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'
    re_waktu3 = '((besok|lusa)|((minggu|bulan)[ ]depan))'
    pesan = pesan.lower()
    kodeMatkul = re.search(re_matkul,pesan).group()
    waktu = re.search(re_waktu1, pesan) or re.search(re_waktu2, pesan) or re.search(re_waktu3, pesan)
    topik = re.sub(waktu.group(), '', pesan)
    posMatkul = -1
    posKata = -1
    posTopik = -1

    tempTopik = topik
    for x in listKosakata:
        kosakata = re.findall(x.kosakata,pesan)
        id_kosakata = x.id
        topik = re.search(x.kosakata+"[ ]([0-9a-z]+([ ]|))+",tempTopik) or re.search(re_matkul+"[ ]([0-9a-z]+([ ]|))+",tempTopik)
        if len(kosakata)>0 :
            topik = topik.group()
            kosakata = kosakata[0]
            posKata = booyer.bmIndex(topik,x.kosakata)
            posMatkul = booyer.bmIndex(topik, kodeMatkul)
            tmp = re.sub(r'[ |]*'+x.kosakata+r'[ |]*','',topik)
            tmp = re.sub(r'[ |]*'+kodeMatkul+r'[ |]*','',tmp)
            posTopik  = booyer.bmIndex(topik,tmp.split(' ')[0])
            break

    tempTopik = ""
    if (posTopik>posMatkul and posTopik<posKata):
        for i in range(posMatkul+len(kodeMatkul),posKata):
            tempTopik = tempTopik + topik[i]
    elif (posTopik<posMatkul and posTopik>posKata):
        for i in range(posKata + len(kosakata), posMatkul):
            tempTopik = tempTopik + topik[i]
    elif posKata<posTopik:
        for i in range(posKata + len(kosakata),len(topik)):
            tempTopik = tempTopik + topik[i]

    topik = tempTopik

    if booyer.bmMatch(waktu.group(),"besok"):
        dtime = datetime.datetime.today() + datetime.timedelta(days=1)
    elif booyer.bmMatch(waktu.group(),"lusa"):
        dtime = datetime.datetime.today() + datetime.timedelta(days=2)
    elif booyer.bmMatch(waktu.group(), "minggu"):
        dtime = datetime.datetime.today() + datetime.timedelta(days=7)
    elif booyer.bmMatch(waktu.group(), "bulan"):
        dtime = datetime.datetime.today() + datetime.timedelta(days=30)
    else:
        dtime = datetime.datetime.strptime(dateParsing(waktu.group()), '%Y-%m-%d')

    tugasBaru = models.Pengingat.objects.filter(matkul=kodeMatkul,
                                 topik_tugas=topik,
                                 tenggat=dtime.date(),
                                 jenis_tugas_id=id_kosakata)
    if len(tugasBaru)>0:
        return {
            "status": "error",
            "header": "Anda telah memiliki task  ini!",
            "pesan": [
                "ID :"+ str(tugasBaru[0].id) +"",
                "deadline : " + str(dtime.date()),
                'kode matkul : ' + kodeMatkul,
                'label : ' + kosakata,
                'topik : ' + topik
            ]
        }
    else:
        tugasBaru = models.Pengingat(matkul=kodeMatkul,
                                     topik_tugas=topik,
                                     tenggat=dtime.date(),
                                     jenis_tugas_id=id_kosakata)
        tugasBaru.save()


    return {
        "status": "ok",
        "header": "Berhasil menambahkan task baru!",
        "pesan": [
            "ID :"+ str(tugasBaru.id) +"",
            "deadline : " + str(dtime.date()),
            'kode matkul : ' + kodeMatkul,
            'label : ' + kosakata,
            'topik : ' + topik
        ]
    }

def checkIsTaskChecker(pesan):
    pesan = pesan.lower()
    listKata = models.DaftarKata.objects.all()
    comp1 = r'.*(apa saja|apakah ada)'
    comp2 = 'deadline'
    c = False
    for x in listKata:
        if booyer.bmMatch(pesan,x.kosakata):
            c = True
            break
    #print(booyer.bmMatch(pesan, comp1))
    #print((booyer.bmMatch(pesan,comp2)))
    #print(c)
    return re.search(comp1,pesan) and (booyer.bmMatch(pesan,comp2) or c)

def taskChecker(pesan : str,listKosakata):
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'
    header = "daftar "
    idPenting = -1
    kataPenting = ''
    for x in listKosakata:
        if booyer.bmMatch(pesan,x.kosakata):
            kataPenting = x.kosakata
            idPenting = x.id
            break

    flag1 = False
    qresult = []
    if idPenting>-1: header = header + kataPenting
    else: header = header + "deadline"

    if(booyer.bmMatch(pesan,'antara') or re.search(re_waktu1+' sampai '+re_waktu1,pesan) or re.search(re_waktu2+' sampai '+re_waktu2,pesan)):
        t1 = re.search(re_waktu1,pesan) or re.search(re_waktu2,pesan)
        tmp  = pesan.replace(t1.group(),'')
        t2 = re.search(re_waktu1,tmp) or re.search(re_waktu2,tmp)
        flag1 = 1==1
        date1 = datetime.datetime.strptime(dateParsing(t1.group()),'%Y-%m-%d')
        date2 = datetime.datetime.strptime(dateParsing(t2.group()), '%Y-%m-%d')
        header = header + " untuk tanggal " + t1.group() + " s.d " + t2.group()

        if idPenting > -1:
            qresult = models.Pengingat.objects.filter(tenggat__range=[date1,date2], jenis_tugas_id=idPenting)
        else:
            qresult = models.Pengingat.objects.filter(tenggat__range=[date1,date2])

    elif booyer.bmMatch(pesan, 'minggu') and booyer.bmMatch(pesan, 'depan'):
        n = re.search('[0-9]+[ ]minggu',pesan)
        n = re.search('[0-9]*',n.group()).group()
        tude = datetime.date.today()
        date1 = tude + datetime.timedelta(days=7*int(n))
        header = header  + " untuk " + str(n) + " minggu kedepan"
        if idPenting > -1:
            qresult = models.Pengingat.objects.filter(tenggat__range=[tude,date1], jenis_tugas_id=idPenting)
        else:
            qresult = models.Pengingat.objects.filter(tenggat__range=[tude,date1])

    elif booyer.bmMatch(pesan, 'hari') and booyer.bmMatch(pesan, 'depan'):
        n = re.search('[0-9]+[ ]hari', pesan)
        n = re.search('[0-9]*', n.group()).group()
        tude = datetime.date.today()
        date1 = tude + datetime.timedelta(days=int(n))
        header = header  + " untuk " + str(n) + " hari kedepan"
        if idPenting>-1:
            qresult = models.Pengingat.objects.filter(tenggat__range=[tude,date1],jenis_tugas_id=idPenting)
        else:
            qresult = models.Pengingat.objects.filter(tenggat__range=[tude,date1])

    elif booyer.bmMatch(pesan, 'hari ini'):
        date1 = datetime.date.today()
        header = header  + " untuk hari ini"
        if idPenting>-1:
            qresult = models.Pengingat.objects.filter(tenggat=date1,jenis_tugas_id=idPenting)
        else:
            qresult = models.Pengingat.objects.filter(tenggat=date1)

    else:
        header = header  + " sejauh ini"
        if idPenting > -1:
            qresult = models.Pengingat.objects.filter(jenis_tugas_id=idPenting)
        else:
            qresult = models.Pengingat.objects.all()

    ret = {
        "status": "ok",
        "header": "",
        "pesan": [ ]
    }

    ret["header"] = header
    for x in qresult:
        kp = models.DaftarKata.objects.filter(id=x.jenis_tugas_id).first()
        ret["pesan"].append("(ID :"+str(x.id)+") "+ str(x.tenggat) + ' - ' + x.matkul + ' - ' +kp.kosakata+ ' - '+ x.topik_tugas)


    return ret

def checkIsDeadlineChekcer(pesan, listKosakata):
    pesan = pesan.lower()
    re_matkul = '(if|ii|ku|ti|ma|fi|el)[1-5][0-9][0-9][0-9]'
    comp2 = 'deadline'
    kosakata = False
    for x in listKosakata:
        kosakata = booyer.bmMatch(pesan,x.kosakata)
        if kosakata:break

    return booyer.bmMatch(pesan, comp2) and kosakata and re.search(re_matkul,pesan)

def deadlineChecker(pesan,listKosakata):
    re_matkul = '(if|ii|ku|ti|ma|fi|el)[1-5][0-9][0-9][0-9]'
    pesan = pesan.lower()
    kodeMatkul = re.search(re_matkul, pesan).group()
    #print(kodeMatkul)
    for x in listKosakata:
        if(booyer.bmMatch(pesan,x.kosakata)):
            kata = x.kosakata
            currTask = models.Pengingat.objects.filter(matkul=kodeMatkul, jenis_tugas=x.id)
            break

    ret = {
        "status": "ok",
        "header": "Daftar deadline untuk " +kata+ " " +kodeMatkul,
        "pesan": [

        ]
    }
    for x in currTask:
        ret["pesan"].append(str(x.id) + ' - ' + x.topik_tugas + ' - ' + str(x.tenggat))
    return ret

def checkIsRenewTask(pesan):
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'

    #cek regex/booyer
    pesan = pesan.lower()
    a = re.search('di[ ]*maju',pesan) or re.search('di[ ]*undur',pesan)
    b = booyer.bmMatch(pesan, "menjadi")
    c = re.search(re_waktu1,pesan) or re.search(re_waktu2,pesan)

    try:
        tmp = pesan.replace(c.group(), '')
        n = re.search('[0-9]+', tmp)

    except:
        return False


    return a and b and c and n

def renewTask(pesan):
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'

    pesan = pesan.lower()
    w= re.search(re_waktu1,pesan) or re.search(re_waktu2,pesan)
    waktu_baru = datetime.datetime.strptime(dateParsing(w.group()), '%Y-%m-%d')
    tmp = pesan.replace(w.group(), '')
    n = re.search('[0-9]+', tmp)
    n = int(n.group())
    dbaseQuery = models.Pengingat.objects.filter(id=n)
    if(len(dbaseQuery)==0):
        return {
            "status": "error",
            "header": "id task tidak ditemukan",
            "pesan": [

            ]
        }

    rec = dbaseQuery.first()


    rec.tenggat = waktu_baru
    rec.save()

    return {
        "status": "ok",
        "header": "Berhasil menyudahi Task dengan id : "+str(n),
        "pesan": [
            'Informasi task yang telah disudahi',
            'Matkul : '+ rec.matkul,
            'Jenis : ' + models.DaftarKata.objects.filter(id=rec.jenis_tugas_id).first().kosakata,
            'Topik : ' + rec.topik_tugas,
            'Tenggat baru : ' + str(rec.tenggat.date()),
        ]
    }

def checkIsMarkTask(pesan):
    re_waktu1 = '([0-9]|[1-3][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([2][0][2-9][0-9]|[2][1-9][0-9][0-9])'
    re_waktu2 = '([2][0][2-9][0-9]|[2][1-9][0-9][0-9])[-/ ]([a-z]+|[1-9]|([1][0-2]|[0][1-9]))[-/ ]([0-9]|[1-3][0-9])'

    # cek regex/booyer
    pesan = pesan.lower()
    a = re.search('mengerjakan', pesan) and re.search('selesai', pesan)
    a = a or (re.search('hapus',pesan) and re.search('task',pesan))
    n = re.search('[0-9]+', pesan)

    return a and n

def markTask(pesan):
    pesan = pesan.lower()
    n = re.search('[0-9]+', pesan)
    n = int(n.group())
    dbQuery = models.Pengingat.objects.filter(id=n)
    task = dbQuery.first()

    ret = {
        "status": "ok",
        "header": "Berhasil menyudahi Task dengan id : "+str(n),
        "pesan": []
    }

    if len(dbQuery)>0:
        ret['pesan'].append('Informasi task yang telah disudahi')
        ret['pesan'].append('Matkul : '+ task.matkul)
        ret['pesan'].append('Jenis : ' + models.DaftarKata.objects.filter(id=task.jenis_tugas_id).first().kosakata)
        ret['pesan'].append('Topik : ' + task.topik_tugas)
        task.delete()
    else:
        ret['status'] = "error"
        ret['header'] ="Id task tidak ada!"
        ret['pesan'] = []
    return ret

def autoFixMessage(pesan):
    return ""

def dateParsing(tanggalan : str):
    bulan = {'januari':1,'februari':2,'maret':3,'april':4,'mei':5,'juni':6,'juli':7,'agustus':8,'september':9,'oktober':10,'november':11,'desember':12}
    yr = re.search('[0-9][0-9][0-9][0-9]',tanggalan)
    tanggalan = tanggalan.replace(yr.group(),'')
    day = re.search('([0-9]+[ /-])|([ /-][0-9]+)',tanggalan)
    #tanggalan = tanggalan.replace(day.group(),'').replace(' ','').replace('/','').replace('-','')
    #print(tanggalan)
    mo = re.search('[ /-]([0-9]+|[a-z]+)[ /-]',tanggalan)
    if(re.search('[0-9][0-9]|[0-9]',mo.group())):
        mo = re.search('([0-9][0-9]|[0-9])',mo.group()).group()
    elif re.search('[a-z]+',mo.group()).group() in bulan.keys():
        tanggalan = re.search('[a-z]+',mo.group()).group()
        mo = bulan[tanggalan]

    return (str(yr.group())+'-'+str(mo)+'-'+str(day.group().replace(' ','').replace('/','').replace('-','').strip()))

def checkTaskIsExist(matkul:str, deadline : datetime.date, topik:str, idkata:int):
    z = models.Pengingat.objects.filter(matkul=matkul,tenggat=deadline,topik_tugas=topik, jenis_tugas_id=idkata)
    return len(z)==0
'''
testing function
'''
#print(checkIsMarkTask("apa yang bisa dilakukan oleh revolusi bot"))