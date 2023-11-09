from flask import Flask, render_template, request, redirect, url_for, session, flash, json, jsonify, Response
from flask_session import Session
from flask_mysqldb import MySQL
import io
import xlwt
#import mysql.connector
import MySQLdb.cursors
import re



app = Flask(__name__)

app.secret_key = '0000'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventaris'
mysql = MySQL(app)
#inventaris
@app.route("/")
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'user_login' in request.form and 'password' in request.form:
        user_login = request.form['user_login']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM table_user WHERE user_login = %s AND password = %s", (user_login, password, ))
        user_login = cursor.fetchone()
        if user_login:
            session['loggedin'] = True
            session['nama'] = user_login['nama_user']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
#inventaris
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('nama', None)
    return redirect(url_for('login'))
#inventaris
@app.route('/index')
def index ():
    return render_template('index.html')
#inventaris
@app.route('/datauser')
def datauser ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM table_user ")
    user = cursor.fetchall()
    return render_template('datauser.html', menu='datauser', data = user)
#inventaris
@app.route('/simpanuser', methods=["POST"])
def simpanuser ():
        user_login     = request.form['user_login']
        password       = request.form['password']
        nama_user      = request.form['nama_user']
        nip            = request.form['nip']
        status         = request.form['status']
        cur            = mysql.connection.cursor()
        cur.execute ("INSERT INTO table_user ( user_login, password, nama_user, nip, status) VALUES(%s,%s,%s,%s,%s)", ( user_login, password, nama_user, nip, status)) 
        mysql.connection.commit()
        return redirect (url_for('datauser'))

#inventaris
@app.route('/updateuser', methods=["POST"])
def updateuser ():
        id_data         = request.form['id_user']
        user_login      = request.form['user_login']
        password        = request.form['password']
        nama_user       = request.form['nama_user']
        nip             = request.form['nip']
        status          = request.form['status']
        cur             = mysql.connection.cursor()
        cur.execute ("UPDATE table_user SET user_login =%s, password =%s, nama_user =%s, nip =%s, status =%s WHERE id_user =%s", (user_login, password, nama_user, nip, status, id_data)) 
        mysql.connection.commit()
        return redirect (url_for('datauser'))

#inventaris
@app.route('/hapususer/<string:id_data>', methods=["GET"])
def hapususer(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_user WHERE id_user =%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('datauser'))

@app.route('/inventaris')
def inventaris ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM table_inventaris")
    inventaris = cursor.fetchall()
    return render_template('inventaris.html', menu='inventaris', data = inventaris)

#inventaris
@app.route('/simpaninventaris', methods=["POST"])
def simpaninventaris ():
        id_inventaris     = request.form['id_inventaris']
        id_barang   = request.form['id_barang']
        tanggal_maintance = request.form['tanggal_maintance']
        maintance_lanjut  = request.form['maintance_lanjut']
        status          = request.form['status']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO inventaris (id_inventaris, id_barang, tanggal_maintance, maintance_lanjut, status) VALUES(%s,%s,%s,%s,%s,%s)", (id_inventaris, id_barang, tanggal_maintance, maintance_lanjut, status)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('inventaris'))

#inventaris
@app.route('/updateinventaris', methods=["POST"])
def updateinventaris ():
        id_inventaris = request.form['id_inventaris']
        id_barang   = request.form['id_barang']
        tanggal_maintance = request.form['tanggal_maintance']
        maintance_lanjut  = request.form['maintance_lanjut']
        status          = request.form['status']
        status            = request.form['status']
        cur               = mysql.connection.cursor()
        cur.execute ("UPDATE table_inventaris SET id_barang =%s, tanggal_maintance =%s, maintance_lanjut =%s status =%s WHERE id_inventaris=%s", (id_inventaris, id_barang, tanggal_maintance, maintance_lanjut, status)) 
        mysql.connection.commit()
        return redirect (url_for('inventaris'))

#inventaris
@app.route('/hapusinventaris/<string:id_data>', methods=["GET"])
def hapusinventaris(id_data):
        cur            = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_inventaris WHERE id_inventaris =%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('inventaris'))

@app.route('/dataapoteker')
def dataapoteker ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM main_user")
    apoteker = cursor.fetchall()
    return render_template('dataapoteker.html', menu='dataapoteker', data = apoteker)
	
@app.route('/simpanapoteker', methods=["POST"])
def simpanapoteker ():
        username       = request.form['username']
        password       = request.form['password']
        nama           = request.form['namaapoteker']
        cur            = mysql.connection.cursor()
        cur.execute ("INSERT INTO main_user (username,password,nama) VALUES(%s,%s,%s)", (username, password, nama)) 
        mysql.connection.commit()
        
        return redirect (url_for('dataadmin'))

@app.route('/datapasien')
def datapasien ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pasien")
    pasien = cursor.fetchall()
    return render_template('datapasien.html', menu='datapasien', data = pasien )

@app.route('/simpanpasien', methods=["POST"])
def simpanpasien ():
        nama            = request.form['nama']
        nik             = request.form['nik']
        jeniskelamin    = request.form['jeniskelamin']
        alamat          = request.form['alamat']
        rt              = request.form['rt']
        rw              = request.form['rw']
        kecamatan       = request.form['kecamatan']
        kelurahan       = request.form['kelurahan']
        tanggallahir    = request.form['tgllahir']
        tanggalmasuk    = request.form['tglmasuk']
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO pasien (nama,nik,jenis_kelamin,alamat,rt,rw,kecamatan,kelurahan,tanggal_lahir,tgl_masuk) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nama,nik,jeniskelamin,alamat,rt,rw,kecamatan,kelurahan,tanggallahir,tanggalmasuk)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('datapasien'))

@app.route('/updatepasien', methods=["POST"])
def updatepasien ():
       
        id_data         = request.form['nik']
        nama            = request.form['nama']
        jenis_kelamin   = request.form['jeniskelamin']
        alamat          = request.form['alamat']
        rt              = request.form['rt']
        rw              = request.form['rw']
        kecamatan       = request.form['kecamatan']
        kelurahan       = request.form['kelurahan']
        tanggal_lahir   = request.form['tgllahir']
        tgl_masuk       = request.form['tglmasuk']
        cur = mysql.connection.cursor()
        cur.execute ("UPDATE pasien SET nama =%s, jenis_kelamin =%s, alamat =%s, rt =%s, rw =%s, kecamatan =%s, kelurahan =%s, tanggal_lahir =%s, tgl_masuk =%s WHERE nik =%s", (nama,jenis_kelamin,alamat,rt,rw,kecamatan,kelurahan,tanggal_lahir,tgl_masuk,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('datapasien'))

@app.route('/hapuspasien/<string:id_data>', methods=["GET"])
def hapuspasien(id_data):
        cur = mysql.connection.cursor()
        cur.execute (" DELETE FROM pasien WHERE nik=%s " , [id_data])
        mysql.connection.commit()
        return redirect (url_for('datapasien'))

@app.route('/detailpasien')
def detailpasien ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pasien ")
    detailpasien = cursor.fetchall()
    return render_template('detailpasien.html', data=detailpasien)

#inventaris
@app.route('/kategori')
def kategori ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM table_kategori")
    kategori = cursor.fetchall()
    return render_template('kategori.html', menu='kategori', data = kategori)
#inventaris
@app.route('/simpankategori', methods=["POST"])
def simpankategori ():
        id_kategori     = request.form['id_kategori']
        nama_kategori   = request.form['nama_kategori']
        detail_kategori = request.form['detail_kategori']
        jenis_kategori  = request.form['jenis_kategori']
        status          = request.form['status']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO table_kategori (id_kategori, nama_kategori, detail_kategori, jenis_kategori, status) VALUES(%s,%s,%s,%s,%s,%s)", (id_kategori, nama_kategori, detail_kategori, jenis_kategori, status)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('kategori'))
#inventaris
@app.route('/updatekategori', methods=["POST"])
def updatekategori ():
        nama_kategori     = request.form['nama_kategori']
        detail_kategori   = request.form['detail_kategori']
        jenis_kategori    = request.form['jenis_kategori']
        status            = request.form['status']
        cur               = mysql.connection.cursor()
        cur.execute ("UPDATE table_kategori SET nama_kategori =%s, detail_kategori =%s, jenis_kategori =%s status =%s WHERE id_kategori=%s", (nama_kategori, detail_kategori, jenis_kategori, status)) 
        mysql.connection.commit()
        return redirect (url_for('kategori'))
#inventaris
@app.route('/hapuskategori/<string:id_data>', methods=["GET"])
def hapuskategori(id_data):
        cur            = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_kategori WHERE id_kategori =%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('kategori'))

#inventaris
@app.route('/merk')
def merk ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM table_merk")
    merk = cursor.fetchall()
    return render_template('merk.html', menu='merk', data = merk)

#inventaris
@app.route('/simpanmerk', methods=["POST"])
def simpanmerk ():
        nama_merk       = request.form['nama_merk']
        detail_merk     = request.form['detail_merk']
        status          = request.form['status']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO table_merk ( nama_merk, detail_merk, status) VALUES(%s,%s,%s)", (  nama_merk, detail_merk, status)) 
        mysql.connection.commit()
        flash("Employee Inserted Successfully")
        return redirect (url_for('merk'))

#inventaris
@app.route('/updatemerk', methods=["POST"])
def updatemerk ():
        id_merk          = request.form['id_merk']
        nama_merk        = request.form['nama_merk']
        detail_merk      = request.form['detail_merk']
        status           = request.form['status']
        cur              = mysql.connection.cursor()
        cur.execute ("UPDATE table_merk SET nama_merk =%s, detail_merk =%s, status =%s WHERE id_merk=%s", (nama_merk, detail_merk, status, id_merk)) 
        mysql.connection.commit()
        return redirect (url_for('merk'))

#inventaris
@app.route('/hapusmerk/<string:id_data>', methods=["GET"])
def hapusmerk(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_merk WHERE id_merk =%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('merk'))

#inventaris
@app.route('/satuan')
def satuan ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM table_satuan")
    satuan = cursor.fetchall()
    return render_template('satuan.html', menu='satuan', data = satuan)

#inventaris
@app.route('/simpansatuan', methods=["POST"])
def simpansatuan ():
        id_satuan        = request.form['id_satuan']
        nama_satuan      = request.form['nama_satuan']
        detail_satuan    = request.form['detail_satuan']
        status           = request.form['status']
        cur              = mysql.connection.cursor()
        cur.execute ("INSERT INTO table_satuan (id_satuan, nama_satuan, detail_satuan, status) VALUES(%s,%s,%s,%s)", (id_satuan, nama_satuan, detail_satuan, status)) 
        mysql.connection.commit()
        flash("Employee Inserted Successfully")
        return redirect (url_for('satuan'))

#inventaris
@app.route('/updatesatuan', methods=["POST"])
def updatesatuan ():
        id_satuan        = request.form['id_satuan']
        nama_satuan      = request.form['nama_satuan']
        detail_satuan    = request.form['detail_satuan']
        status           = request.form['status']
        cur              = mysql.connection.cursor()
        cur.execute ("UPDATE table_satuan SET nama_satuan =%s, detail_satuan =%s, status =%s WHERE id_satuan=%s", (nama_satuan, detail_satuan, status, id_satuan)) 
        mysql.connection.commit()
        return redirect (url_for('satuan'))

#inventaris
@app.route('/hapussatuan/<string:id_data>', methods=["GET"])
def hapussatuan(id_data):
        cur            = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_satuan WHERE id_satuan= '%s'", (id_data))
        mysql.connection.commit()
        return redirect (url_for('satuan'))


#inventaris
@app.route('/supplier')
def supplier ():
    cur         = mysql.connection.cursor()
    cur.execute("SELECT * FROM table_supplier")
    supplier    = cur.fetchall()
    return render_template('supplier.html', menu='', submenu='supplier', data = supplier)
 
#inventaris
@app.route('/simpansupplier', methods=["POST"])
def simpansupplier ():
        id_supplier      = request.form['id_supplier']
        nama_supplier    = request.form['nama_supplier']
        alamat_supplier  = request.form['alamat_supplier']
        detail_supplier  = request.form['detail_supplier']
        status           = request.form['status']
        cur              = mysql.connection.cursor()
        cur.execute ("INSERT INTO table_supplier (id_supplier, nama_supplier,alamat_supplier,detail_supplier,status) VALUES(%s,%s,%s,%s,%s)", (id_supplier,nama_supplier,alamat_supplier,detail_supplier,status)) 
        mysql.connection.commit()
        flash("Employee Inserted Successfully")
        return redirect (url_for('supplier'))
#inventaris
@app.route('/hapussupplier/<string:id_data>', methods=["GET"])
def hapusanalgetik(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM table_supplier WHERE id_supplier= %s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('supplier'))

#inventaris
@app.route('/updatesupplier', methods=["POST"])
def updateanalgetik ():
        id_data          = request.form['id_supplier']
        nama_supplier    = request.form['nama_supplier']
        alamat_supplier  = request.form['alamat_supplier']
        detail_supplier  = request.form['detail_supplier']
        status           = request.form['status']
        cur              = mysql.connection.cursor()
        cur.execute ("UPDATE supplier SET nama_supplier =%s, alamat_supplier=%s, detail_supplier=%s, status=%s WHERE id_supplier=%s", (nama_supplier,alamat_supplier,detail_supplier,status,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('supplier'))

@app.route('/antibiotik')
def antibiotik ():
    cur                 = mysql.connection.cursor()
    cur.execute("SELECT * FROM antibiotik")
    antibiotik = cur.fetchall()
    return render_template('antibiotik.html', menu='kategori', submenu='antibiotik', data = antibiotik)

@app.route('/simpanantibiotik', methods=["POST"])
def simpanantibiotik ():
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO antibiotik (nama_obatab,jenisab,harga,stok) VALUES(%s,%s,%s,%s)", (nama_obat,jenis,harga,stok)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('antibiotik'))

@app.route('/updateantibiotik', methods=["POST"])
def updateantibiotik ():
        id_data         = request.form['id_antibiotik']
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("UPDATE antibiotik SET nama_obatab =%s, jenisab=%s, harga=%s, stok=%s WHERE id_antibiotik=%s", (nama_obat,jenis,harga,stok,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('antibiotik'))

@app.route('/hapusantibiotik/<string:id_data>', methods=["GET"])
def hapusantibiotik(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM antibiotik WHERE id_antibiotik =%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('antibiotik'))


@app.route('/antihistemi')
def antihistemi ():
    cursor              = mysql.connection.cursor()
    cursor.execute("SELECT * FROM antihistemi")
    antihistemi = cursor.fetchall()
    return render_template('antihistemi.html', menu='kategori', submenu='antihistemi', data = antihistemi)

@app.route('/simpanantihistemi', methods=["POST"])
def simpanantihistemi ():
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO antihistemi (nama_obatah,jenisah,harga,stok) VALUES(%s,%s,%s,%s)", (nama_obat,jenis,harga,stok)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('antihistemi'))

@app.route('/updateantihistemi', methods=["POST"])
def updateantihistemi ():
        id_data         = request.form['id_histemi']
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("UPDATE antihistemi SET nama_obatah =%s, jenisah=%s, harga=%s, stok=%s WHERE id_histemi=%s", (nama_obat,jenis,harga,stok,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('antihistemi'))

@app.route('/hapusantihistemi/<string:id_data>', methods=["GET"])
def hapusantihistemi(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM antihistemi WHERE id_histemi=%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('antihistemi'))

@app.route('/antinyeri')
def antinyeri ():
    cursor              = mysql.connection.cursor()
    cursor.execute("SELECT * FROM antinyeri")
    antinyeri = cursor.fetchall()
    return render_template('antinyeri.html', menu='kategori', submenu='antinyeri', data = antinyeri)    

@app.route('/simpanantinyeri', methods=["POST"])
def simpanantinyeri ():
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO antinyeri (nama_obatan,jenisan,harga,stok) VALUES(%s,%s,%s,%s)", (nama_obat,jenis,harga,stok)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('antinyeri'))

@app.route('/updateantinyeri', methods=["POST"])
def updateantinyeri ():
        id_data         = request.form['id_antinyeri']
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("UPDATE antinyeri SET nama_obatan =%s, jenisan=%s, harga=%s, stok=%s WHERE id_antinyeri=%s", (nama_obat,jenis,harga,stok,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('antinyeri'))

@app.route('/hapusantinyeri/<string:id_data>', methods=["GET"])
def hapusantinyeri(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM antinyeri WHERE id_antinyeri=%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('antinyeri'))

@app.route('/antipiretik')
def antipiretik ():
    cursor              = mysql.connection.cursor()
    cursor.execute("SELECT * FROM antipiretik")
    antipiretik = cursor.fetchall()
    return render_template('antipiretik.html', menu='kategori', submenu='antipiretik', data = antipiretik)

@app.route('/simpanantipiretik', methods=["POST"])
def simpanantipiretik ():
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("INSERT INTO antipiretik (nama_obatap,jenisap,harga,stok) VALUES(%s,%s,%s,%s)", (nama_obat,jenis,harga,stok)) 
        mysql.connection.commit()
        
        flash("Employee Inserted Successfully")
        return redirect (url_for('antipiretik'))

@app.route('/updateantipiretik', methods=["POST"])
def updateantipiretik ():
        id_data         = request.form['id_antipiretik']
        nama_obat       = request.form['namaobat']
        jenis           = request.form['jenis']
        harga           = request.form['harga']
        stok            = request.form['stok']
        cur             = mysql.connection.cursor()
        cur.execute ("UPDATE antipiretik SET nama_obatap =%s, jenisap=%s, harga=%s, stok=%s WHERE id_antipiretik=%s", (nama_obat,jenis,harga,stok,id_data)) 
        mysql.connection.commit()
        return redirect (url_for('antipiretik'))

@app.route('/hapusantipiretik/<string:id_data>', methods=["GET"])
def hapusantipiretik(id_data):
        cur             = mysql.connection.cursor()
        cur.execute ("DELETE FROM antipiretik WHERE id_antipiretik=%s", (id_data))
        mysql.connection.commit()
        return redirect (url_for('antipiretik'))

@app.route('/transaksi')
def transaksi ():
    return render_template('transaksi.html')

@app.route('/tambahtransaksi', methods=["POST"])
def tambahtransaksi ():
        nik               = request.form['nik']
        nama_pasien       = request.form['nama_pasien']
        jenis_kelamin     = request.form['jeniskelamin']
        diagnosa          = request.form['diagnosa']
        kategori          = request.form['kategori']
        no_bpjs           = request.form['nobpjs']
        nama_dokter       = request.form['namadokter']
        tgl_periksa       = request.form['tglperiksa']
        obat              = request.form['obat']
        no_hp             = request.form['nohp']
        cur               = mysql.connection.cursor()
        cur.execute ("INSERT INTO transaksi (nik, nama_pasien,jenis_kelamin, diagnosa, kategori, no_bpjs, nama_dokter, tgl_periksa, obat, no_hp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nik,nama_pasien,jenis_kelamin, diagnosa, kategori, no_bpjs, nama_dokter, tgl_periksa, obat, no_hp)) 
        mysql.connection.commit()

        msg = 'Logged in successfully !'
        return redirect (url_for('transaksi'))

@app.route('/laporan1')
def laporan1 ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transaksi ")
    transaksi = cursor.fetchall()
    return render_template('laporan1.html', menu='laporan' ,submenu='laporan1', data=transaksi)

@app.route('/detailtransaksi')
def detailtransaksi ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transaksi ")
    detail = cursor.fetchone()
    return render_template('laporan1.html', menu='laporan' ,submenu='laporan1', data=detail)

@app.route('/laporanpasien')
def laporanpasien ():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transaksi ")
    laporanpasien = cursor.fetchall()
    return render_template('laporanpasien.html', menu='laporan', submenu='laporanpasien', data=laporanpasien)

@app.route('/downloadexcel')
def downloadexcel():
  cursor = mysql.connection.cursor()
  
  cursor.execute("SELECT id_transaksi,nik, nama_pasien, jenis_kelamin, diagnosa, kategori, no_bpjs, nama_dokter, tgl_periksa, obat, no_hp FROM transaksi ")
  result = cursor.fetchall()
  
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Data Pasien')
  
  #add headers
  sh.write(0, 0, 'Id Transaksi')
  sh.write(0, 1, 'NIK')
  sh.write(0, 2, 'Nama Pasien')
  sh.write(0, 3, 'Jenis Kelamin')
  sh.write(0, 4, 'Gejala')
  sh.write(0, 5, 'Kategori')
  sh.write(0, 6, 'No BPJS')
  sh.write(0, 7, 'Nama Dokter')
  sh.write(0, 8, 'Tanggal Periksa')
  sh.write(0, 9, 'Obat')
  sh.write(0, 10, 'No Hp')
  
  idx = 0
  for row in result:
   sh.write(idx+1, 0, row[0])
   sh.write(idx+1, 1, row[1])
   sh.write(idx+1, 2, row[2])
   sh.write(idx+1, 3, row[3])
   sh.write(idx+1, 4, row[4])
   sh.write(idx+1, 5, row[5])
   sh.write(idx+1, 6, row[6])
   sh.write(idx+1, 7, row[7])
   sh.write(idx+1, 8, row[8])
   sh.write(idx+1, 9, row[9])
   sh.write(idx+1, 10, row[10])
   idx += 1
  
  workbook.save(output)
  output.seek(0)
  
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=data_pasien_berobat.xls"})
                    
if __name__  == "__main__":
    app.run (debug=True)