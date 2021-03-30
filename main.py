#import requests
import json
import requests
import sys, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
#import qdarkstyle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5 import uic
from PyQt5 import QtCore as qtc
import dateutil.parser

from Tab import Ui_tabs
from Rutmodal import Ui_Rutmodal
from UserBooking import Ui_UserBooking
from AceptarReserva import Ui_Aceptar_Reserva
from Add_obsCab import Ui_Add_ObsCab 
from addBooking import Ui_addBooking
from Booking_AceptarReserva import Ui_Booking_aceptarReserva
from Booking_cabinsAvailable import Ui_Booking_cabinsAvailable
from cabinsAvailable import Ui_cabinsAvailable
from Disable_cab import Ui_Disable_cab
from editBooking import Ui_editBooking
from editPrecio import Ui_editPrecio
from EditUser import Ui_EditUser
from fixedUp import Ui_fixedUp
from host import Ui_dialog
from newUser import Ui_newUser
from obsCab import Ui_obsCab

global IPs 
IPs = "127.0.0.1:8007"

class Host(QtWidgets.QDialog, Ui_dialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_dialog.__init__(self)
        self.setupUi(self)
        #== Eventos ==# 
        self.link.clicked.connect(self.linked)


    def linked(self):
        global IPs
        IPs = self.ip.text()
        self.tab = Tabs()
        self.close()
        self.tab.show()

class Tabs(QtWidgets.QWidget, Ui_tabs):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Ui_tabs.__init__(self)
        #super(base_1, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        #-- Table customer --#
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)       
        self.tableWidget.setHorizontalHeaderLabels("Contacto;Correo;Nombre;Procedencia;RUT;Telefono".split(";"))        
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)

        #-- Table Reservas--#
        self.tableWidgetC.setColumnCount(7)
        self.tableWidgetC.setRowCount(3)       
        self.tableWidgetC.setHorizontalHeaderLabels("Reserva;Nombre;Rut;Procedencia;Telefono;Correo;Contacto".split(";"))        
        self.tableWidgetC.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetC.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetC.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetC.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.tableWidgetC.setWordWrap(False)
        self.tableWidgetC.setSortingEnabled(False)
        self.tableWidgetC.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        self.tableWidgetC.horizontalHeader().setHighlightSections(False)
        self.tableWidgetC.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetC.setAlternatingRowColors(True)

        #-- Table Cabins --#
        self.tableWidgetCab.setColumnCount(2)
        self.tableWidgetCab.setRowCount(3)       
        self.tableWidgetCab.setHorizontalHeaderLabels("Cabañas;Precio".split(";"))        
        self.tableWidgetCab.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetCab.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetCab.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetCab.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.tableWidgetCab.setWordWrap(False)
        self.tableWidgetCab.setSortingEnabled(False)
        self.tableWidgetCab.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        self.tableWidgetCab.horizontalHeader().setHighlightSections(False)
        self.tableWidgetCab.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetCab.setAlternatingRowColors(True)
        # Ocultar encabezado vertical
        #self.tableWidgetC.vertself.tabla.veronfticalHeader().setVisible(False)
        #self.tableWidgetCab.verticalHeader().setDefaultSectionSize(30)


        
        #== EVENTOS == #
        #self.host = Host()
        #self.host.show()
        #--Tab calendar--#
        self.reservas_tab.clicked.connect(self.reservas)
        
        # set up a timer that automatically updates every second
        self.lcd.setMinimumWidth(80)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        #--

        #--Tab customer--#
        self.deployCustomers()
        self.tableWidget.itemDoubleClicked.connect(self.doubleClickCustomer)
        self.update.clicked.connect(self.updateUser)
        self.eliminar.clicked.connect(self.remove)
        self.sendEmail.clicked.connect(self.emailSend)
        self.buscar.clicked.connect(self.searchRut)
        self.editR.clicked.connect(self.reservasUser)

        #--Tab cabins--#
        now = QDate.currentDate()
        self.fecha.setDate(now)
        self.deployReservas()
        self.fecha.dateChanged.connect(self.buscarF)
        self.fecha.dateChanged.connect(self.labelDate)
        self.labelDate()
        
        self.deployCabins()
        self.tableWidgetCab.itemDoubleClicked.connect(self.doubleClickCab)
        self.edp.clicked.connect(self.editP)
    
    def labelDate(self):
        # label to show the long name form of the selected date
        # format US style like "Thursday, February 20, 2020"
        select = self.fecha.date()
        weekday, month = select.dayOfWeek(), select.month()
        day, year = str(select.day()), str(select.year())
        week_day, word_month = QDate.longDayName(weekday), QDate.longMonthName(month)
        self.label_date.setText(week_day + " " + day + " " + word_month + ", " + year)
    
    def showTime(self):
        # keep the current time updated
        time = QTime.currentTime()
        text = time.toString("hh:mm")
        if time.second() % 2 == 0:
            text.replace(text[2], '')
        self.lcd.display(text)

    @qtc.pyqtSlot()
    def deployCabins(self):
        
        r = requests.get("http://{}/cabanas".format(IPs))
        cabins = r.json()['data']
        #print(cabins)
        self.tableWidgetCab.setRowCount(0)  
        for i, cab in enumerate(cabins):
            self.tableWidgetCab.insertRow(i)
            self.tableWidgetCab.setItem(i, 0, QTableWidgetItem(str(cab['ID'])))
            self.tableWidgetCab.setItem(i, 1, QTableWidgetItem(str(cab['Precio'])))
    
    def doubleClickCab(self):
        cab = [dato.text() for dato in self.tableWidgetCab.selectedItems()]
        
        self.obs_cab = Observacion_Cabana(cab)
        self.obs_cab.show()



    def reservas(self):
        self.reservas_rut = Reservas_rut()
        self.reservas_rut.submitted.connect(self.update_deployCustomers)
        self.reservas_rut.show()

        #self.newUser = Nuevo_usuario()
        #self.newUser.submitted2.connect(self.update_deployCustomers)
        #self.reservas_rut.show()
    
    def reservasUser(self):
        rut = self.rut.text()
        self.reservas_user = Reservas_Usuario(rut)
        self.reservas_user.show()


    def deployReservas(self):
        
        date = self.fecha.date().toString(Qt.ISODate)          
        r = requests.get("http://{}/ocupado/{}".format(IPs, date))
        cabinsdisp = r.json()['data']
        #print(cabinsdisp)
        Cabs = { "0": 0, "1": 1, "2": 2} #Todas disponibles 
        for disp in cabinsdisp: #No disponibles    
            i = disp['IDcabin'] -1 
            self.tableWidgetC.setItem(i, 0, QTableWidgetItem('Reservado'))
            self.tableWidgetC.setItem(i, 1, QTableWidgetItem(disp['Nombre']))
            self.tableWidgetC.setItem(i, 2, QTableWidgetItem(disp['RUT']))
            self.tableWidgetC.setItem(i, 3, QTableWidgetItem(disp['Procedencia']))
            self.tableWidgetC.setItem(i, 4, QTableWidgetItem(str(disp['Telefono'])))
            self.tableWidgetC.setItem(i, 5, QTableWidgetItem(disp['Correo']))
            self.tableWidgetC.setItem(i, 6, QTableWidgetItem(disp['Contacto']))
            Cabs.pop(str(i))
        
        for i in Cabs.values(): #Disponibles
            self.tableWidgetC.setItem(i, 0, QTableWidgetItem('Disponible'))
            self.tableWidgetC.setItem(i, 1, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 2, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 3, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 4, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 5, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 6, QTableWidgetItem(''))

    def buscarF(self):
        
        date = self.fecha.date().toString(Qt.ISODate)          
        r = requests.get("http://{}/ocupado/{}".format(IPs,date))
        cabinsdisp = r.json()['data']
        Cabs = { "0": 0, "1": 1, "2": 2} #Todas disponibles 
        for disp in cabinsdisp: #No disponibles  
            i = disp['IDcabin'] - 1
            self.tableWidgetC.setItem(i, 0, QTableWidgetItem('Reservado'))
            self.tableWidgetC.setItem(i, 1, QTableWidgetItem(disp['Nombre']))
            self.tableWidgetC.setItem(i, 2, QTableWidgetItem(disp['RUT']))
            self.tableWidgetC.setItem(i, 3, QTableWidgetItem(disp['Procedencia']))
            self.tableWidgetC.setItem(i, 4, QTableWidgetItem(str(disp['Telefono'])))
            self.tableWidgetC.setItem(i, 5, QTableWidgetItem(disp['Correo']))
            self.tableWidgetC.setItem(i, 6, QTableWidgetItem(disp['Contacto']))
            Cabs.pop(str(i))
        
        for i in Cabs.values(): #Disponibles
            self.tableWidgetC.setItem(i, 0, QTableWidgetItem('Disponible'))
            self.tableWidgetC.setItem(i, 1, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 2, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 3, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 4, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 5, QTableWidgetItem(''))
            self.tableWidgetC.setItem(i, 6, QTableWidgetItem(''))


    def deployCustomers(self):
        result = requests.get('http://{}//clientes'.format(IPs))  
        customers = result.json()['data']
        #print(customers)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(customers):
            #print(row_number)
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data.values()):
                #print(data)
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        firstUser = customers[0]
        self.rut.setText(firstUser['RUT'])
        self.nombre.setText(firstUser['Nombre'])
        self.telefono.setText(str(firstUser['Telefono']))
        self.correo.setText(firstUser['Correo'])
        self.procedencia.setText(firstUser['Procedencia'])
        self.contacto.setText(firstUser['Contacto'])

    
    @qtc.pyqtSlot(str,str,str,str,str,str)
    def update_deployCustomers(self, rut, nombre, telefono, correo, procedencia, contacto):
        self.rut.setText(rut)
        self.nombre.setText(nombre)
        self.telefono.setText(telefono)
        self.correo.setText(correo)
        self.procedencia.setText(procedencia)
        self.contacto.setText(contacto)
        
        result = requests.get('http://{}//clientes'.format(IPs))  
        customers = result.json()['data']

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(customers):
            #print(row_number)
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data.values()):
                #print(data)
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    

    def doubleClickCustomer(self):
        
        customer = [dato.text() for dato in self.tableWidget.selectedItems()]
        
        self.rut.setText(customer[4])
        self.nombre.setText(customer[2])
        self.telefono.setText(customer[5])
        self.correo.setText(customer[1])
        self.procedencia.setText(customer[3])
        self.contacto.setText(customer[0])
    
    def updateUser(self):
        #customer = [dato.text() for dato in self.tableWidget.selectedItems()]

        rut = self.rut.text()
        nombre = self.nombre.text()
        procedencia = self.procedencia.text()
        telefono = self.telefono.text()
        correo = self.correo.text()
        contacto = self.contacto.text()

        customer = [contacto, correo, nombre, procedencia, rut, telefono]
        self.editUser = Editar_Usuario(customer)
        self.editUser.submitted.connect(self.update_deployCustomers)

        #self.newUser = Nuevo_usuario()
        #self.newUser.submitted2.connect(self.update_deployCustomers)


        self.editUser.show()
    
    def remove(self):
        rut = self.rut.text()
        if(rut == "00000000-0"):
            QMessageBox.warning(self,"Warning", "No se puede eliminar el rut 00000000-0 (Deshabilitador de cabañas)", QMessageBox.Ok)
        else:
            ret = QMessageBox.warning(self,"Warning", "¿Está seguro que desea eliminar el cliente?", QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                r = requests.delete('http://{}/clientes/{}'.format(IPs, rut))
                r2= r.json()
                if(r2['message'] == 'Internal Server Error'):
                    QMessageBox.warning(self,"Warning", "No se pudo eliminar, debido a que posee reservas disponibles. Para poder removerlo necesita eliminar todo su historial de reservas.", QMessageBox.Ok)
                else:
                    QMessageBox.information(self,"Information", "El cliente se eliminó satisfactoriamente", QMessageBox.Ok)
                    self.deployCustomers()
    
    def emailSend(self):
        def simpleSend(recver,subject,messag):
            defaultSend="igmavamailtest@gmail.com"
            defaultPass="ismabaya"
            return sendMail(defaultSend,defaultPass,recver,subject,messag)

        def sendMail(sender,sendpass,recver,subject,messag):
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = recver
            message['Subject'] = subject
            message.attach(MIMEText(messag, 'plain'))
            text = message.as_string()
            try:
                session = smtplib.SMTP('smtp.gmail.com', 587)
                session.starttls()
                session.login(sender, sendpass)
                session.sendmail(sender, recver, text)
                session.quit()
                QMessageBox.information(self,"", "Mensaje enviado!", QMessageBox.Ok)
                return "Correo Enviado"
            except:
                QMessageBox.warning(self,"", "Ocurrió un error!", QMessageBox.Ok)
                return "Ocurrio Error"
    
        def moroseMail(name,debt,mail):
            asunto="Importante: Comunicado sobre deuda Cabañas Igmava."
            cuerpo="""Estimado/a Sr./Sra. {},
    
            Le escribimos para comunircarle que actualmente debe el pago de ${} por su estadía.
            Le rogamos realize el deposito a la cuenta bancaria indicada lo antes posible.
            Si tiene alguna consulta puede contactarnos al telefono indicado.
    
            Cuenta: XXXX-XXXX-XXXX
            Fono: XXXX-XXXX-XXXX""".format(name,debt)
            return simpleSend(mail,asunto,cuerpo)
    
    
        result = moroseMail("Abada Kadabra",50000,"igmavamailtest@gmail.com")
    
    def searchRut(self):
        rut = self.search.text()
        if(rut == ''):
            self.deployCustomers()
        else:
            try:
                r = requests.get('http://{}//clientes/{}'.format(IPs, rut))
                customer = r.json()['data'][0]
                #print(customer)
                self.tableWidget.setRowCount(1) 
                self.tableWidget.setItem(0, 0, QTableWidgetItem(customer['Contacto']))
                self.tableWidget.setItem(0, 1, QTableWidgetItem(customer['Correo']))
                self.tableWidget.setItem(0, 2, QTableWidgetItem(customer['Nombre']))
                self.tableWidget.setItem(0, 3, QTableWidgetItem(customer['Procedencia']))
                self.tableWidget.setItem(0, 4, QTableWidgetItem(customer['RUT']))
                self.tableWidget.setItem(0, 5, QTableWidgetItem(str(customer['Telefono'])))
            except:
                print("Rut inexistente")
    
    def editP(self):
        self.editPrecio = Editar_Precio()
        self.editPrecio.submitted.connect(self.deployCabins)
        self.editPrecio.show()

class Observacion_Cabana(QtWidgets.QWidget, Ui_obsCab):
    def __init__(self, cab):
        QtWidgets.QWidget.__init__(self)
        Ui_obsCab.__init__(self)
        self.setupUi(self)
        self.cab_id = cab[0]

        #-- Table customer --#
        self.obs.setColumnCount(5)   
        self.obs.setHorizontalHeaderLabels("ID,Tipo,Fecha,Descripcion,Arreglado".split(","))        
        self.obs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.obs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.obs.setSelectionMode(QAbstractItemView.SingleSelection)
        self.obs.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.obs.setWordWrap(False)
        self.obs.setSortingEnabled(False)
        self.obs.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        self.obs.horizontalHeader().setHighlightSections(False)
        self.obs.horizontalHeader().setStretchLastSection(True)
        self.obs.setAlternatingRowColors(True)
        self.obs.verticalHeader().setDefaultSectionSize(30)

        #== EVENTOS ==#

        self.despliegueObs()
        self.deshabilitar.clicked.connect(self.deshabilitarCab)
        #self.deshabilitar.clicked.connect(self.deshabilitarCab)
        self.obs.itemDoubleClicked.connect(self.arr)

        self.add_obs.clicked.connect(self.obser)


    def despliegueObs(self):
        r = requests.get('http://{}/observaciones/{}'.format(IPs, self.cab_id))
        observaciones = r.json()['data']
        #print(observaciones)

        self.obs.setRowCount(0)
        for row_number, ob in enumerate(observaciones):
            self.obs.insertRow(row_number)
            self.obs.setItem(row_number, 0, QTableWidgetItem(str(ob['ID'])))
            self.obs.setItem(row_number, 1, QTableWidgetItem(ob['Tipo']))
            self.obs.setItem(row_number, 2, QTableWidgetItem(dateutil.parser.parse(ob['Fecha']).strftime('%Y-%m-%d')))
            self.obs.setItem(row_number, 3, QTableWidgetItem(ob['Descripcion'])) 
            self.obs.setItem(row_number, 4, QTableWidgetItem(str(ob['Arreglado'])))
    
    @qtc.pyqtSlot()
    def update_despliegueObs(self):
        r = requests.get('http://{}/observaciones/{}'.format(IPs, self.cab_id))
        observaciones = r.json()['data']
        #print(observaciones)

        self.obs.setRowCount(0)
        for row_number, ob in enumerate(observaciones):
            self.obs.insertRow(row_number)
            self.obs.setItem(row_number, 0, QTableWidgetItem(str(ob['ID'])))
            self.obs.setItem(row_number, 1, QTableWidgetItem(ob['Tipo']))
            self.obs.setItem(row_number, 2, QTableWidgetItem(dateutil.parser.parse(ob['Fecha']).strftime('%Y-%m-%d')))
            self.obs.setItem(row_number, 3, QTableWidgetItem(ob['Descripcion']))
            self.obs.setItem(row_number, 4, QTableWidgetItem(str(ob['Arreglado'])))

    def deshabilitarCab(self):
        self.desh = Deshabilitar_Cabana(self.cab_id)
        self.desh.submitted.connect(self.update_despliegueObs)
        self.desh.show()
    
    def obser(self):
        self.ob = Anadir_Observacion_Cabana(self.cab_id)
        self.ob.submitted.connect(self.update_despliegueObs)
        self.ob.show()
    
    def arr(self):
        cabObs = [dato.text() for dato in self.obs.selectedItems()]

        self.arre = Arreglado_Cabana(cabObs, self.cab_id)
        self.arre.submitted.connect(self.update_despliegueObs)
        self.arre.show()

class Anadir_Observacion_Cabana(QtWidgets.QDialog, Ui_Add_ObsCab):

    submitted = qtc.pyqtSignal()

    def __init__(self, id_cab):
        QDialog.__init__(self)
        Ui_Add_ObsCab.__init__(self)
        self.setupUi(self)
        self.cab_id = id_cab

        self.tipo.textChanged.connect(self.validar_tipo)
        self.descripcion.textChanged.connect(self.validar_descripcion)

        #== EVENTOS ==#
        self.aceptar.clicked.connect(self.accept)
        self.cancelar.clicked.connect(self.cancel)
    
    def accept(self):
        if self.validar_descripcion() and self.validar_tipo():
            now = QDate.currentDate()
            date = now.toString(Qt.ISODate)   
            tipo = self.tipo.text()
            descripcion = self.descripcion.toPlainText()
            obsCab = {'cabin': self.cab_id, 'tipo': tipo, 'fecha': date, 'descripcion': descripcion, 'arreglado': '0'}
            r = requests.post('http://{}/observaciones/'.format(IPs), json = obsCab)
            self.submitted.emit()
            self.close()
            QMessageBox.information(self, "Formulario correcto", "Observacion agregada a la cabaña", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Formulario incorrecto", "Verifique si los datos estan ingresados correctamente", QMessageBox.Ok)

    
    def validar_descripcion(self):
        descripcion = self.descripcion.toPlainText()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', descripcion, re.I)
        if descripcion == "":
            self.descripcion.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.descripcion.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.descripcion.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_tipo(self):
        tipo = self.tipo.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', tipo, re.I)
        if tipo == "":
            self.tipo.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.tipo.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.tipo.setStyleSheet("border: 1px solid green;")
            return True
    
    def cancel(self):
        self.close()

class Deshabilitar_Cabana(QtWidgets.QDialog, Ui_Disable_cab):

    submitted = qtc.pyqtSignal()

    def __init__(self, id_cab):
        QDialog.__init__(self)
        Ui_Disable_cab.__init__(self)
        self.setupUi(self)

        self.cab_id = id_cab
        self.aceptar.clicked.connect(self.aceptarDesh)

        #== EVENTOS ==#
        self.tipo.textChanged.connect(self.validar_tipo)
        self.descripcion.textChanged.connect(self.validar_descripcion)
        self.cancelar.clicked.connect(self.cancel)

    
     
    def aceptarDesh(self):       
        if self.validar_descripcion() and self.validar_tipo():
            dateCheckin = self.checkin.date().toString(Qt.ISODate)
            dateCheckout = self.checkout.date().toString(Qt.ISODate)
            tipo = self.tipo.text()
            descripcion = self.descripcion.toPlainText()
            
            #Observacion cabaña, deshabilitada
            obsCab = {'cabin': self.cab_id, 'tipo': tipo, 'fecha': dateCheckin, 'descripcion': descripcion, 'arreglado': '0'}
            r = requests.post('http://{}/observaciones/'.format(IPs), json = obsCab)
            #print(r)
            self.submitted.emit()
    
            #Deshabilitar cabaña
            data = {'RUT': '00000000-0', 'in': dateCheckin, 'out': dateCheckout, 'costo': 0 , 'pagado': 0, 'cabins': [int(self.cab_id)]}
            r2 = requests.post('http://{}//reservas'.format(IPs), json = data)
            #print(r2)
            QMessageBox.information(self, "Formulario correcto", "Cabaña deshabilitada!", QMessageBox.Ok)
            self.close()
        else:
            QMessageBox.warning(self, "Formulario incorrecto", "Verifique si los datos estan ingresados correctamente", QMessageBox.Ok)

    def validar_descripcion(self):
        descripcion = self.descripcion.toPlainText()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', descripcion, re.I)
        if descripcion == "":
            self.descripcion.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.descripcion.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.descripcion.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_tipo(self):
        tipo = self.tipo.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', tipo, re.I)
        if tipo == "":
            self.tipo.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.tipo.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.tipo.setStyleSheet("border: 1px solid green;")
            return True
    def cancel(self):
        self.close()

class Arreglado_Cabana(QtWidgets.QDialog, Ui_fixedUp):
    submitted = qtc.pyqtSignal()
    def __init__(self, cabObs, cab_id):
        QDialog.__init__(self)
        Ui_fixedUp.__init__(self)
        self.setupUi(self)

        self.id = cabObs[0]
        self.tipo = cabObs[1]
        self.fecha = cabObs[2]
        self.descripcion = cabObs[3]
        self.cab_id = cab_id
        self.aceptar.clicked.connect(self.accept)
    
    def accept(self):
        if self.checkBox.isChecked() == True:
            obsCab = {'cabin': self.cab_id, 'tipo': self.tipo, 'fecha': self.fecha, 'descripcion': self.descripcion, 'arreglado': '1'}
            r = requests.put('http://{}/observaciones/{}'.format(IPs).format(self.id), json = obsCab)
            self.submitted.emit()
            self.close()
        else:    
            self.close()

class Reservas_Usuario(QtWidgets.QMainWindow, Ui_UserBooking):
    def __init__(self, rut):
        QtWidgets.QMainWindow.__init__(self)
        Ui_UserBooking.__init__(self)
        self.setupUi(self)
        
        self.r = rut #rut


        #-- Table customer --#
        self.reservasRUT.setColumnCount(6)   
        self.reservasRUT.setHorizontalHeaderLabels("ID-Reserva,RUT,Check-out,Check-in,Costo,Pagado".split(","))        
        self.reservasRUT.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.reservasRUT.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.reservasRUT.setSelectionMode(QAbstractItemView.SingleSelection)
        self.reservasRUT.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.reservasRUT.setWordWrap(False)
        self.reservasRUT.setSortingEnabled(False)
        self.reservasRUT.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        self.reservasRUT.horizontalHeader().setHighlightSections(False)
        self.reservasRUT.horizontalHeader().setStretchLastSection(True)
        self.reservasRUT.setAlternatingRowColors(True)
        self.reservasRUT.verticalHeader().setDefaultSectionSize(30)


        #== EVENTOS ==#
        self.deployReservas(rut)
        self.reservasRUT.itemDoubleClicked.connect(self.doubleClickReserva)
        self.editarReserva.clicked.connect(self.updateReserva)
        self.eliminarReserva.clicked.connect(self.remove)
    
    def deployReservas(self, rut):
        r = requests.get('http://{}/reservasRut/{}'.format(IPs, rut))
        reservas = r.json()['data']

        self.reservasRUT.setRowCount(0)
        for row_number, customer in enumerate(reservas):
            self.reservasRUT.insertRow(row_number)

            #dt=dateutil.parser.parse('Mon, 14 Dec 2020 00:00:00 GMT')
            #print(dt.strftime('%Y-%m-%d'))

            self.reservasRUT.setItem(row_number, 0, QTableWidgetItem(str(customer['ID'])))
            self.reservasRUT.setItem(row_number, 1, QTableWidgetItem(customer['RUT']))
            self.reservasRUT.setItem(row_number, 2, QTableWidgetItem(dateutil.parser.parse(customer['Check_in']).strftime('%Y-%m-%d')))
            self.reservasRUT.setItem(row_number, 3, QTableWidgetItem(dateutil.parser.parse(customer['Check_out']).strftime('%Y-%m-%d')))
            self.reservasRUT.setItem(row_number, 4, QTableWidgetItem(str(customer['Costo'])))
            self.reservasRUT.setItem(row_number, 5, QTableWidgetItem(str(customer['Pagado'])))
        
        if(reservas != []):
            firstReserva = reservas[0]
            self.id.setText(str(firstReserva['ID']))
            self.rut.setText(firstReserva['RUT'])
            self.check_in.setText(dateutil.parser.parse(firstReserva['Check_in']).strftime('%Y-%m-%d'))
            self.check_out.setText(dateutil.parser.parse(firstReserva['Check_out']).strftime('%Y-%m-%d'))
            self.costo.setText(str(firstReserva['Costo']))
            self.pagado.setText(str(firstReserva['Pagado']))
        else:
            self.id.setText('')
            self.rut.setText('')
            self.check_in.setText('')
            self.check_out.setText('')
            self.costo.setText('')
            self.pagado.setText('')

            self.editarReserva.hide()
            self.eliminarReserva.hide()
    
    @qtc.pyqtSlot(str,str,str,str,str,str)
    def update_deployReservas(self, ids, rut, checkout, checkin, costo, pagado):
        self.id.setText(ids)
        self.rut.setText(rut)
        self.check_in.setText(checkout)
        self.check_out.setText(checkin)
        self.costo.setText(costo)
        self.pagado.setText(pagado)

        r = requests.get('http://{}/reservasRut/{}'.format(IPs, rut))
        reservas = r.json()['data']
        #print(reservas)

        self.reservasRUT.setRowCount(0)
        for row_number, customer in enumerate(reservas):
            self.reservasRUT.insertRow(row_number)

            #dt=dateutil.parser.parse('Mon, 14 Dec 2020 00:00:00 GMT')
            #print(dt.strftime('%Y-%m-%d'))

            self.reservasRUT.setItem(row_number, 0, QTableWidgetItem(str(customer['ID'])))
            self.reservasRUT.setItem(row_number, 1, QTableWidgetItem(customer['RUT']))
            self.reservasRUT.setItem(row_number, 2, QTableWidgetItem(dateutil.parser.parse(customer['Check_in']).strftime('%Y-%m-%d')))
            self.reservasRUT.setItem(row_number, 3, QTableWidgetItem(dateutil.parser.parse(customer['Check_out']).strftime('%Y-%m-%d')))
            self.reservasRUT.setItem(row_number, 4, QTableWidgetItem(str(customer['Costo'])))
            self.reservasRUT.setItem(row_number, 5, QTableWidgetItem(str(customer['Pagado'])))
        
        if(reservas != []):
            firstReserva = reservas[0]
            self.id.setText(str(firstReserva['ID']))
            self.rut.setText(firstReserva['RUT'])
            self.check_in.setText(dateutil.parser.parse(firstReserva['Check_in']).strftime('%Y-%m-%d'))
            self.check_out.setText(dateutil.parser.parse(firstReserva['Check_out']).strftime('%Y-%m-%d'))
            self.costo.setText(str(firstReserva['Costo']))
            self.pagado.setText(str(firstReserva['Pagado']))
        else:
            self.id.setText('')
            self.rut.setText('')
            self.check_in.setText('')
            self.check_out.setText('')
            self.costo.setText('')
            self.pagado.setText('')
        
        
       
    def doubleClickReserva(self):
        reserva = [dato.text() for dato in self.reservasRUT.selectedItems()]
        #print(reserva)
        
        self.id.setText(reserva[0])
        self.rut.setText(reserva[1])
        self.check_in.setText(reserva[2])
        self.check_out.setText(reserva[3])
        self.costo.setText(reserva[4])
        self.pagado.setText(reserva[5])
    
    def updateReserva(self):
        #customer = [dato.text() for dato in self.tableWidget.selectedItems()]

        ids = self.id.text()
        rut = self.rut.text()
        check_in = self.check_in.text()
        check_out = self.check_out.text()
        #correo = self.correo.text()
        #contacto = self.contacto.text()

        reserva = [ids, rut, check_in, check_out]
        self.editR = Editar_Reserva(reserva)
        self.editR.submitted.connect(self.update_deployReservas)
        
        self.editR.show()
        #self.editR.submitted.connect(self.update_deployCustomers)
    
    def remove(self):
        ids = self.id.text()
        ret = QMessageBox.warning(self,"Warning", "¿Está seguro que desea eliminar la reserva?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            r = requests.delete('http://{}/reservas/{}'.format(IPs, ids))
            QMessageBox.information(self,"Information", "La reserva se eliminó satisfactoriamente!", QMessageBox.Ok)
            self.deployReservas(self.r)
    
class Editar_Reserva(QtWidgets.QDialog, Ui_editBooking):
    
    submitted = qtc.pyqtSignal(str,str,str,str,str,str)
    
    def __init__(self, reserva):
        QDialog.__init__(self)
        Ui_editBooking.__init__(self)
        self.setupUi(self)
        #print(reserva)
        
        now = QDate.currentDate()
        self.checkin.setDate(now)
        self.checkin.setMinimumDate(now)
        self.checkout.setMinimumDate(now)
        #print(now)

        self.id = reserva[0]
        self.rut = reserva[1]
        #print(customer['Nombre'])
        #self.username.setText(['Nombre'])
        self.rut_user.setText(self.rut)

        #== EVENTOS ==#

        self.precio.clicked.connect(self.disponibilidad)
        self.cancelar.clicked.connect(self.cancel)
        
    def disponibilidad(self):
     
        #Verificar si hay reserva 

        desc = self.desc.value()
        dateCheckin = self.checkin.date().toString(Qt.ISODate)
        dateCheckout = self.checkout.date().toString(Qt.ISODate)
        #print(dateCheckout)
        r = requests.get("http://{}/disponible/{}/{}".format(IPs, dateCheckin,dateCheckout))
        result = r.json()['data'][0]['Cabins']

   
        self.cabinsAvailable = Disponibilidad_reserva_usuario([self.rut, result, desc, dateCheckin, dateCheckout, self.id])
        self.cabinsAvailable.submitted2.connect(self.move_data)
        self.cabinsAvailable.show()
        self.hide()
    
    @qtc.pyqtSlot(str,str,str,str,str,str)
    def move_data(self, ids, rut, datecheckout, datecheckin, costo, pagado):
        self.submitted.emit(ids, rut, datecheckout, datecheckin, costo, pagado)
    
    def cancel(self):
        self.close()

class Disponibilidad_reserva_usuario(QtWidgets.QDialog, Ui_Booking_cabinsAvailable):

    submitted2 = qtc.pyqtSignal(str,str,str,str,str,str)
         
    def __init__(self, customer):
        QDialog.__init__(self)
        Ui_Booking_cabinsAvailable.__init__(self)
        self.setupUi(self)
        #print(customer)   
        self.rut = customer[0]
        self.desc = customer[2]
        self.cabins = customer[1]
        self.dateCheckin = customer[3]
        self.dateCheckout = customer[4]
        self.id = customer[5]
        
        if 1 not in self.cabins:
            self.cab1_2.hide()
        
        if 2 not in self.cabins:
            self.cab2_2.hide()

        if 3 not in self.cabins:
            self.cab3_2.hide()
        
        if(self.cabins == []):
            self.label.setText("NO HAY DISPONIBILIDAD")
            self.precio.hide()


    
        # == EVENTOS == #

        self.precio.clicked.connect(self.aceptarR)
        self.cancelar.clicked.connect(self.cancel)


    def aceptarR(self):
        #--#
        self.cabs = []
        if self.cab1_2.isChecked() == True:
            self.cabs.append(1)
            
        if self.cab2_2.isChecked() == True:
            self.cabs.append(2)
            
        if self.cab3_2.isChecked() == True:
            self.cabs.append(3)  

                    
        if(self.cabs != []):
            self.aceptarReserva = Aceptar_Reserva_Usuario([self.rut, self.cabs, self.desc, self.dateCheckin, self.dateCheckout, self.id])
            self.aceptarReserva.submitted3.connect(self.move_data)
            self.close()
            self.aceptarReserva.show()
        else:
            QMessageBox.warning(self,"Warning", "No ha seleccionado ninguna cabaña!", QMessageBox.Ok)
    
    @qtc.pyqtSlot(str,str,str,str,str,str)
    def move_data(self, ids, rut, datecheckout, datecheckin, costo, pagado):
        self.submitted2.emit(ids, rut, datecheckout, datecheckin, costo, pagado)

    
    def cancel(self):
         self.close()

class Aceptar_Reserva_Usuario(QtWidgets.QDialog, Ui_Booking_aceptarReserva):
    submitted3 = qtc.pyqtSignal(str,str,str,str,str,str)

    def __init__(self, customer):
        QDialog.__init__(self)
        Ui_Booking_aceptarReserva.__init__(self)
        self.setupUi(self)

        self.rut = customer[0]
        self.desc = customer[2]
        self.cabs = customer[1]
        self.dateCheckin = customer[3]
        self.dateCheckout = customer[4]
        self.id = customer[5]

        self.totalCosto = 0
        for cab in self.cabs:
            #Me falta considerar los dias
            r = requests.get('http://{}//cabanas/{}'.format(IPs, cab))
            cabana = r.json()['data'][0]
            costo = cabana['Precio'] - cabana['Precio']*(self.desc/100)
            #print(costo)
            self.totalCosto = int(self.totalCosto + costo) 

        #print(self.totalCosto)
        self.precio.setText(str(self.totalCosto))

        
        # == EVENTOS == #

        self.aceptar.clicked.connect(self.aceptarReserva)
        self.cancelar.clicked.connect(self.cancel)

    def aceptarReserva(self):
        data = {'RUT': self.rut, 'in': self.dateCheckin, 'out': self.dateCheckout, 'costo': self.totalCosto , 'pagado': '0', 'cabins': self.cabs}

        r = requests.put('http://{}/reservas/{}'.format(IPs, self.id), json = data)  
        #QMessageBox.information(self,"", "Reserva ingresada", QMessageBox.Ok)
        self.submitted3.emit(self.id, self.rut, self.dateCheckout, self.dateCheckin, str(self.totalCosto), '0')
        self.close()
    
    def cancel(self):
        self.close()
            
class Editar_Usuario(QtWidgets.QDialog, Ui_EditUser):

    submitted = qtc.pyqtSignal(str,str,str,str,str,str)

    def __init__(self, customer):
        QDialog.__init__(self)
        Ui_EditUser.__init__(self)
        self.setupUi(self)

        self.rut = customer[4]
        self.nombre.setText(customer[2])
        self.telefono.setText(customer[5])
        self.correo.setText(customer[1])
        self.procedencia.setText(customer[3])
        self.contacto.setText(customer[0])

        self.nombre.textChanged.connect(self.validar_nombre)
        self.correo.textChanged.connect(self.validar_email)
        self.telefono.textChanged.connect(self.validar_telefono)
        self.procedencia.textChanged.connect(self.validar_procedencia)
        self.contacto.textChanged.connect(self.validar_contacto)

        #== EVENTOS ==#

        self.aceptar.clicked.connect(self.confirmed)
        self.cancelar.clicked.connect(self.cancel)
    
    def confirmed(self):
        if self.validar_nombre() and self.validar_email() and self.validar_telefono() and self.validar_procedencia() and self.validar_contacto():
            rut = self.rut
            nombre = self.nombre.text()
            procedencia = self.procedencia.text()
            telefono = self.telefono.text()
            correo = self.correo.text()
            contacto = self.contacto.text()
            customer = {'nombre': nombre, 'procedencia': procedencia, 'telefono': telefono, 'correo': correo, 'contacto': contacto}
            r = requests.put('http://{}/clientes/{}'.format(IPs, rut), json = customer)
            #FALTA VERIFICAR EL 'r' ( 200 = OK, 404 = ERROR)
            QMessageBox.information(self, "Formulario correcto", "Usuario actualizado", QMessageBox.Ok)
            #print(r)
            #if(r == "<Response [200]>"):
            self.submitted.emit(rut, nombre, telefono, correo, procedencia, contacto)
            self.close()
           
        else:          
            QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Ok)
    
    def cancel(self):
        self.close()
 
    
    #==VALIDACIONES==#
    def validar_telefono(self):
        telefono = self.telefono.text()
        validar = re.match (('^[0-9]+$')  , telefono)
        if telefono == "":
            self.rut.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.telefono.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.telefono.setStyleSheet("border: 1px solid green;")
            return True

    def validar_nombre(self):
        nombre = self.nombre.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
        if nombre == "":
            self.nombre.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.nombre.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.nombre.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_procedencia(self):
        procedencia = self.procedencia.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', procedencia, re.I)
        if procedencia == "":
            self.procedencia_rutcia.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.procedencia.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.procedencia.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_email(self):
        email = self.correo.text()
        validar = re.match('^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$', email, re.I)
        if email == "":
            self.correo.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.correo.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.correo.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_contacto(self):
        contacto = self.contacto.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', contacto, re.I)
        if contacto == "":
            self.contacto.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.contacto.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.contacto.setStyleSheet("border: 1px solid green;")
            return True

class Reservas_rut(QtWidgets.QDialog, Ui_Rutmodal):
    
    submitted = qtc.pyqtSignal(str,str,str,str,str,str)

    def __init__(self):
        QDialog.__init__(self)
        Ui_Rutmodal.__init__(self)
        self.setupUi(self)

        #== EVENTOS == #
        self.reservar_rut.clicked.connect(self.reservar)
        self.nuevo_usuario.clicked.connect(self.newUser)
    
    def reservar(self):
        rut = self.rut_edit.text()
        #print(rut)
        #try:
        r = requests.get('http://{}//clientes/{}'.format(IPs,rut))
        try:
            if(r.json()['data'] == []):
                QMessageBox.information(self,"", "Usuario no existe", QMessageBox.Ok)
            else:
                customer = r.json()['data'][0]
                self.addReserve = Agregar_reserva(customer)
                self.close()
                self.addReserve.show()
        except:
            QMessageBox.information(self,"", "Ingrese rut(NO VACÍO)", QMessageBox.Ok)
    
    def newUser(self):
        self.newUsuario = Nuevo_usuario()
        self.newUsuario.submitted2.connect(self.moveData)

        self.close()
        self.newUsuario.show()
    
    @qtc.pyqtSlot(str,str,str,str,str,str)
    def moveData(self, rut, nombre, telefono, correo, procedencia, contacto):
        self.submitted.emit(rut, nombre, telefono, correo, procedencia, contacto)
    
class Agregar_reserva(QtWidgets.QDialog, Ui_addBooking):
    def __init__(self, customer):
        QDialog.__init__(self)
        Ui_addBooking.__init__(self)
        self.setupUi(self)

        #self.fechayhora = QtGui.QDateTimeEdit(self)

        now = QDate.currentDate()
        self.checkin.setDate(now)
        self.checkin.setMinimumDate(now)
        self.checkout.setMinimumDate(now)

        self.rut = customer['RUT']
        #print(customer['Nombre'])
        self.username.setText(customer['Nombre'])
        self.rut_user.setText(customer['RUT'])

        #== EVENTOS ==#

        self.precio.clicked.connect(self.disponibilidad)
        self.cancelar.clicked.connect(self.cancel)
        
    
    def disponibilidad(self):
     
        #Verificar si hay reserva 

        desc = self.desc.value()
        dateCheckin = self.checkin.date().toString(Qt.ISODate)
        dateCheckout = self.checkout.date().toString(Qt.ISODate)
        r = requests.get("http://{}/disponible/{}/{}".format(IPs, dateCheckin,dateCheckout))
        result = r.json()['data'][0]['Cabins']

        self.cabinsAvailable = Cabañas_disponibles(self.rut, result, desc, dateCheckin, dateCheckout)
        self.cabinsAvailable.show()
    
    def cancel(self):
        self.close()

class Cabañas_disponibles(QtWidgets.QDialog, Ui_cabinsAvailable):

    def __init__(self, rut, cabins, desc, dateCheckin, dateCheckout):
        QDialog.__init__(self)
        Ui_cabinsAvailable.__init__(self)
        self.setupUi(self)
        
        self.rut = rut
        self.desc = desc
        self.cabins = cabins
        self.dateCheckin = dateCheckin
        self.dateCheckout = dateCheckout
        
        if 1 not in self.cabins:
            self.cab1.hide()
        
        if 2 not in self.cabins:
            self.cab2.hide()

        if 3 not in self.cabins:
            self.cab3.hide()
        
        if(cabins == []):
            self.label.setText("NO HAY DISPONIBILIDAD")
            self.precio.hide()


    
        # == EVENTOS == #

        self.precio.clicked.connect(self.aceptarR)
        self.cancelar.clicked.connect(self.cancel)


    def aceptarR(self):

        #--#
        self.cabs = []
        if self.cab1.isChecked() == True:
            self.cabs.append(1)
            
        if self.cab2.isChecked() == True:
            self.cabs.append(2)
            
        if self.cab3.isChecked() == True:
            self.cabs.append(3)              
        
        if(self.cabs != []):
            self.aceptarReserva = Aceptar_reserva(self.rut, self.cabs, self.desc, self.dateCheckin, self.dateCheckout)
            self.close()
            self.aceptarReserva.show()
        else:
            QMessageBox.warning(self,"Warning", "No ha seleccionado ninguna cabaña!", QMessageBox.Ok)
    
    def cancel(self):
        self.close()
       
class Aceptar_reserva(QtWidgets.QDialog, Ui_Aceptar_Reserva):
    def __init__(self, rut, cabs, desc, dateCheckin, dateCheckout):
        QDialog.__init__(self)
        Ui_Aceptar_Reserva.__init__(self)
        self.setupUi(self)

        self.rut = rut
        self.desc = desc
        self.cabs = cabs
        self.dateCheckin = dateCheckin
        self.dateCheckout = dateCheckout


        self.totalCosto = 0
        for cab in cabs:
            #Me falta considerar los dias
            r = requests.get('http://{}//cabanas/{}'.format(IPs, cab))
            cabana = r.json()['data'][0]
            costo = cabana['Precio'] - cabana['Precio']*(desc/100)
            self.totalCosto = int(self.totalCosto + costo) 

        self.precio.setText(str(self.totalCosto))

        
        # == EVENTOS == #

        self.aceptar.clicked.connect(self.aceptarReserva)
        self.cancelar.clicked.connect(self.cancel)


    def aceptarReserva(self):
        data = {'RUT': self.rut, 'in': self.dateCheckin, 'out': self.dateCheckout, 'costo': self.totalCosto , 'pagado': '0', 'cabins': self.cabs}


        r = requests.post('http://{}/reservas'.format(IPs), json = data)
        QMessageBox.information(self,"", "Reserva ingresada", QMessageBox.Ok)
        self.close()
    
    def cancel(self):
        self.close()
   
class Nuevo_usuario(QtWidgets.QDialog, Ui_newUser):

    submitted2 = qtc.pyqtSignal(str,str,str,str,str,str)

    def __init__(self):
        QDialog.__init__(self)
        Ui_newUser.__init__(self)
        self.setupUi(self)

        self.rut.textChanged.connect(self.validar_rut)
        self.nombre.textChanged.connect(self.validar_nombre)
        self.correo.textChanged.connect(self.validar_email)
        self.telefono.textChanged.connect(self.validar_telefono)
        self.procedencia.textChanged.connect(self.validar_procedencia)
        self.contacto.textChanged.connect(self.validar_contacto)


        self.aceptar.clicked.connect(self.confirmed)

    
    def confirmed(self):
        if self.validar_rut() and self.validar_nombre() and self.validar_email() and self.validar_telefono() and self.validar_procedencia() and self.validar_contacto():
            rut = self.rut.text()
            nombre = self.nombre.text()
            procedencia = self.procedencia.text()
            telefono = self.telefono.text()
            correo = self.correo.text()
            contacto = self.contacto.text()
            customer = {'RUT': rut, 'nombre': nombre, 'procedencia': procedencia, 'telefono': telefono, 'correo': correo, 'contacto': contacto}
            r = requests.post('http://{}/clientes'.format(IPs), json = customer)
            resp = r.json()
            if(resp['message'] == 'Internal Server Error'):
                QMessageBox.warning(self, "Warning", "¡El rut del usuario ingresado ya existe!", QMessageBox.Ok)
            else:       
                customer = {'RUT': rut, 'Nombre': nombre, 'Procedencia': procedencia, 'Telefono': telefono, 'Correo': correo, 'Contacto': contacto}
                self.submitted2.emit(rut, nombre, telefono, correo, procedencia, contacto)
                self.addReserve = Agregar_reserva(customer)
                QMessageBox.information(self, "Formulario correcto", "Usuario ingresado en el sistema", QMessageBox.Ok)
                self.close()
                self.addReserve.show()
        else:          
            QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Ok)
 
    def validar_rut(self):
        rut = self.rut.text()
        validar = re.match ('^[0-9]{7,}[-][0-9Kk]$', rut, re.I)
        if rut == "":
            self.rut.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.rut.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.rut.setStyleSheet("border: 1px solid green;")
            return True

    def validar_telefono(self):
        telefono = self.telefono.text()
        validar = re.match (('^[0-9]+$')  , telefono)
        if telefono == "":
            self.rut.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.telefono.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.telefono.setStyleSheet("border: 1px solid green;")
            return True

    def validar_nombre(self):
        nombre = self.nombre.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
        if nombre == "":
            self.nombre.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.nombre.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.nombre.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_procedencia(self):
        procedencia = self.procedencia.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', procedencia, re.I)
        if procedencia == "":
            self.procedencia.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.procedencia.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.procedencia.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_email(self):
        email = self.correo.text()
        validar = re.match('^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$', email, re.I)
        if email == "":
            self.correo.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.correo.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.correo.setStyleSheet("border: 1px solid green;")
            return True
    
    def validar_contacto(self):
        contacto = self.contacto.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', contacto, re.I)
        if contacto == "":
            self.contacto.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.contacto.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.contacto.setStyleSheet("border: 1px solid green;")
            return True
    
class Editar_Precio(QtWidgets.QDialog, Ui_editPrecio):
     submitted = qtc.pyqtSignal()
     
     def __init__(self):
        QDialog.__init__(self)
        Ui_editPrecio.__init__(self)
        self.setupUi(self)
    
        #Consulta del precio actual a la bd
        r = requests.get("http://{}/cabanas/1".format(IPs))
        precioActual = r.json()['data'][0]['Precio']
        self.precio_label.setText(str(precioActual))
        self.precio.setValue(precioActual)

        #== EVENTOS ==#
        self.confirmar.clicked.connect(self.aceptar)
        self.cancelar.clicked.connect(self.cancel)

     def aceptar(self):
        precio = self.precio.value()
        precioObj = { 'precio': precio }
        ret = QMessageBox.warning(self,"Warning", "¿Está seguro que desea cambiar el precio de las cabañas?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            r = requests.put('http://{}/cabanas/precio'.format(IPs), json = precioObj)
            self.submitted.emit()
            self.close()
    
     def cancel(self):
         self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Host()
    ex.show()
    sys.exit(app.exec_())