# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newUser.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newUser(object):
    def setupUi(self, newUser):
        newUser.setObjectName("newUser")
        newUser.resize(484, 765)
        newUser.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(newUser)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("font: 57 14pt \"Ubuntu\";\n"
"font-weight: bold;")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.rut = QtWidgets.QLineEdit(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rut.sizePolicy().hasHeightForWidth())
        self.rut.setSizePolicy(sizePolicy)
        self.rut.setObjectName("rut")
        self.horizontalLayout_6.addWidget(self.rut)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.gridLayout_7.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_6, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nombre = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        self.nombre.setObjectName("nombre")
        self.horizontalLayout.addWidget(self.nombre)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_6.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.procedencia = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.procedencia.sizePolicy().hasHeightForWidth())
        self.procedencia.setSizePolicy(sizePolicy)
        self.procedencia.setObjectName("procedencia")
        self.horizontalLayout_2.addWidget(self.procedencia)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 3, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.telefono = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.telefono.sizePolicy().hasHeightForWidth())
        self.telefono.setSizePolicy(sizePolicy)
        self.telefono.setObjectName("telefono")
        self.horizontalLayout_3.addWidget(self.telefono)
        spacerItem3 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 4, 0, 1, 2)
        self.groupBox_4 = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.correo = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.correo.sizePolicy().hasHeightForWidth())
        self.correo.setSizePolicy(sizePolicy)
        self.correo.setObjectName("correo")
        self.horizontalLayout_4.addWidget(self.correo)
        spacerItem4 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 5, 0, 1, 2)
        self.groupBox_5 = QtWidgets.QGroupBox(newUser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setStyleSheet("font: 57 11pt \"Ubuntu\";\n"
"font-weight:bold;")
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.contacto = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contacto.sizePolicy().hasHeightForWidth())
        self.contacto.setSizePolicy(sizePolicy)
        self.contacto.setObjectName("contacto")
        self.horizontalLayout_5.addWidget(self.contacto)
        spacerItem5 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 6, 0, 1, 2)
        self.cancelar = QtWidgets.QPushButton(newUser)
        self.cancelar.setObjectName("cancelar")
        self.gridLayout.addWidget(self.cancelar, 7, 0, 1, 1)
        self.aceptar = QtWidgets.QPushButton(newUser)
        self.aceptar.setObjectName("aceptar")
        self.gridLayout.addWidget(self.aceptar, 7, 1, 1, 1)

        self.retranslateUi(newUser)
        QtCore.QMetaObject.connectSlotsByName(newUser)
        newUser.setTabOrder(self.rut, self.nombre)
        newUser.setTabOrder(self.nombre, self.procedencia)
        newUser.setTabOrder(self.procedencia, self.telefono)
        newUser.setTabOrder(self.telefono, self.correo)
        newUser.setTabOrder(self.correo, self.contacto)
        newUser.setTabOrder(self.contacto, self.aceptar)
        newUser.setTabOrder(self.aceptar, self.cancelar)

    def retranslateUi(self, newUser):
        _translate = QtCore.QCoreApplication.translate
        newUser.setWindowTitle(_translate("newUser", "Nuevo usuario"))
        self.label_6.setText(_translate("newUser", "Nuevo usuario"))
        self.groupBox_6.setTitle(_translate("newUser", "Rut"))
        self.groupBox.setTitle(_translate("newUser", "Nombre"))
        self.groupBox_2.setTitle(_translate("newUser", "Procedencia"))
        self.groupBox_3.setTitle(_translate("newUser", "Telefono"))
        self.groupBox_4.setTitle(_translate("newUser", "Correo"))
        self.groupBox_5.setTitle(_translate("newUser", "Contacto"))
        self.cancelar.setText(_translate("newUser", "Cancelar"))
        self.aceptar.setText(_translate("newUser", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newUser = QtWidgets.QDialog()
    ui = Ui_newUser()
    ui.setupUi(newUser)
    newUser.show()
    sys.exit(app.exec_())
