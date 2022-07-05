# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:52:01 2022

@author: fulapuser
"""

import sys
import os
#os.chdir(os.path.expanduser('~'))
sys.path.append(r'C:\Users\fulapuser\Desktop\camlsinst_withfunctions')
from camlsinstallfunctions import (sanity_check_wsl_enabled, 
    sanity_check_ubuntu_installed, sanity_check_camels_installed, 
    sanity_check_pyenv_installed, enable_wsl, set_ubuntu_user_password,
    ubuntu_installer, install_epics_base, install_camels, 
    setup_python_environment, run_camels, sanity_check_epics_installed,
    install_pyenv)

# from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
# from PyQt5.QtCore import QCoreApplication
# from PyQt5.QtGui import QIcon, QPixmap
# from gui.installer_window import Ui_InstallerWindow

# class InstallerWindow(QMainWindow, Ui_InstallerWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUi(self)
#         self.setWindowTitle('CAMELS Installer')
#         self.setWindowIcon(QIcon('../graphics/CAMELS.svg'))
#         image = QPixmap()
#         image.load('../graphics/CAMELS_Logo.png')
#         self.image_label = QLabel()
#         self.image_label.setPixmap(image)
#         self.centralwidget.layout().addWidget(self.image_label, 0, 0, 4, 1)

#         self.radioButton_full.clicked.connect(self.install_type_change)
#         self.radioButton_custom.clicked.connect(self.install_type_change)
#         self.install_type_change()

#         self.pushButton_cancel.clicked.connect(self.close)
#         self.pathButton_CAMELS.set_path(os.path.join(os.path.expanduser('~'), 'CAMELS'))
#         # self.checkBox_wsl.clicked.connect(self.install_wsl_change)

#         self.groupBox_progress.setHidden(True)
#         self.resize(self.minimumSizeHint())

#     def install_wsl_change(self):
#         wsl = self.checkBox_wsl.isChecked()
#         self.checkBox_epics.setEnabled(wsl)

#     def install_type_change(self):
#         full = self.radioButton_full.isChecked()
#         self.groupBox_custom_install.setHidden(full)
#         self.resize(self.minimumSizeHint())


def full_sanity_check(camels_install_path,):
    if sanity_check_wsl_enabled() == 0:
        enable_wsl()
    else:
        print('Passed WSL enabled check')
        pass
    
    if sanity_check_ubuntu_installed() == 0:
        password_ubuntu_input = set_ubuntu_user_password()
        ubuntu_installer(password_ubuntu_input)
    else:
        print('Passed ubuntu installed check')
        password_ubuntu_input = set_ubuntu_user_password()
        pass
    
    if sanity_check_epics_installed() == 0:
        install_epics_base(password_ubuntu_input)
    else:
        print('Passed EPICS installed check')
        pass
    if sanity_check_camels_installed(camels_install_path) == 0:
        install_camels()
    else:
        print('Passed CAMELS installed check')
        pass
    if sanity_check_pyenv_installed() == 0:
        install_pyenv()
        setup_python_environment()
    else:
        print('Passed pyenv installed check')
        setup_python_environment()
    
    run_camels()
    

    
        
            
        
        
        
    


if __name__ == '__main__':
    full_sanity_check(os.path.expanduser('~'))
    # app = QCoreApplication.instance()
    # if app is None:
    #     app = QApplication(sys.argv)
    # ui = InstallerWindow()
    # ui.show()
    # app.exec_()

    