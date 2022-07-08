# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:52:01 2022

@author: fulapuser
"""

import sys
import os
from camlsinstallfunctions import (sanity_check_wsl_enabled, 
        sanity_check_ubuntu_installed, sanity_check_camels_installed,
        sanity_check_pyenv_installed, enable_wsl, set_ubuntu_user_password,
        ubuntu_installer, install_epics_base, install_camels,
        setup_python_environment, run_camels, sanity_check_epics_installed,
        install_pyenv)
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from gui.installer_window import Ui_InstallerWindow


class InstallThread(QThread):
    progress_signal = pyqtSignal(int)
    info_signal = pyqtSignal(str)

    def __init__(self, camels_install_path, install_wsl_bool, install_epics_bool,
                 install_camels_bool, install_pythonenv_bool):
        super().__init__()
        self.camels_install_path = camels_install_path
        self.checkbox_install_wsl = install_wsl_bool
        self.checkbox_install_epics = install_epics_bool
        self.checkbox_install_camels = install_camels_bool
        self.checkbox_install_pythonenv = install_pythonenv_bool

    def run(self):
        full_sanity_check(self.camels_install_path, self.checkbox_install_wsl,
                          self.checkbox_install_epics,self.checkbox_install_camels,
                          self.checkbox_install_pythonenv,
                          self.progress_signal, self.info_signal)


class InstallerWindow(QMainWindow, Ui_InstallerWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CAMELS Installer')
        self.setWindowIcon(QIcon('./graphics/CAMELS.svg'))
        image = QPixmap()
        image.load('./graphics/CAMELS_Logo.png')
        self.image_label = QLabel()
        self.image_label.setPixmap(image)
        self.centralwidget.layout().addWidget(self.image_label, 0, 0, 4, 1)

        self.radioButton_full.clicked.connect(self.install_type_change)
        self.radioButton_custom.clicked.connect(self.install_type_change)
        self.install_type_change()

        self.pushButton_cancel.clicked.connect(self.close)
        self.pathButton_CAMELS.set_path(os.path.join(os.path.expanduser('~'), 'CAMELS'))
        self.pushButton_install.clicked.connect(self.start_install)
        # self.checkBox_wsl.clicked.connect(self.install_wsl_change)

        self.groupBox_progress.setHidden(True)
        self.resize(self.minimumSizeHint())
        if len(sys.argv) > 1:
            if sys.argv[1] == 'rerun':
                if 'custom' in sys.argv:
                    self.radioButton_custom.setChecked(True)
                    if 'wsl' in sys.argv:
                        self.checkBox_wsl.setChecked(True)

                        ### MISSING checkBox values !!! ###

                    self.pathButton_CAMELS.set_path(sys.argv[-1])
                self.start_install()

    def start_install(self):
        if self.radioButton_full.isChecked():
            camels_install_path = os.path.join(os.path.expanduser('~'), 'CAMELS')
            self.install_thread = InstallThread(camels_install_path,
                                                install_wsl_bool=True,
                                                install_epics_bool=True,
                                                install_camels_bool=True,
                                                install_pythonenv_bool=True,)

        if self.radioButton_custom.isChecked():
            camels_install_path = self.pathButton_CAMELS.get_path()
            wsl_install_bool = self.checkBox_wsl.isChecked()
            epics_install_bool = self.checkBox_epics.isChecked()
            camels_install_bool = self.checkBox_camels.isChecked()
            pythonenv_install_bool = self.checkBox_python.isChecked()
            self.install_thread = InstallThread(camels_install_path, wsl_install_bool,
                                                epics_install_bool, camels_install_bool,
                                                pythonenv_install_bool,)
            self.install_thread.progress_signal.connect(self.progressBar_installation.setValue)
            self.install_thread.info_signal.connect(self.label_current_job.setText)
            self.install_thread.start()
            self.groupBox_questions.setHidden(True)
            self.groupBox_progress.setHidden(False)

    def install_wsl_change(self):
        wsl = self.checkBox_wsl.isChecked()
        self.checkBox_epics.setEnabled(wsl)

    def install_type_change(self):
        full = self.radioButton_full.isChecked()
        self.groupBox_custom_install.setHidden(full)
        self.resize(self.minimumSizeHint())


def full_sanity_check(camels_install_path, checkbox_install_wsl,
                          checkbox_install_epics, checkbox_install_camels,
                          checkbox_install_pythonenv,
                      progress_signal=None, info_signal=None):
    # print(f'{checkbox_install_pythonenv=},{checkbox_install_wsl=},{checkbox_install_epics=},{checkbox_install_camels=},')
    # check to see if install script is in the windows startup folder and removes it.
    if os.path.exists(os.path.join(os.path.expanduser('~'), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
                                                            r"\Startup\rerun_camels_installer.exe")):
        os.remove(os.path.join(os.path.expanduser('~'), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
                                                            r"\Startup\rerun_camels_installer.exe"))
    if os.path.exists(os.path.join(os.path.expanduser('~'), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
                                                            "\Startup\camels_exe_path.txt")):
        os.remove(os.path.join(os.path.expanduser('~'), "AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
                                                            "\Startup\camels_exe_path.txt"))

    if checkbox_install_wsl:
        print('checkboxinstallwsl true')
        if sanity_check_wsl_enabled() == 0:
            print(sys.argv[0])
            enable_wsl(sys.argv[0],
                       checkbox_install_wsl,
                       checkbox_install_epics,
                       checkbox_install_camels,
                       checkbox_install_pythonenv,)
        else:
            print('Passed WSL enabled check')
            pass

        if sanity_check_ubuntu_installed() == 0:
            password_ubuntu_input = set_ubuntu_user_password()
            ubuntu_installer(password_ubuntu_input)
        else:
            print('Passed ubuntu installed check')
            pass
    if progress_signal:
        progress_signal.emit(25)
    if checkbox_install_epics:
        if sanity_check_epics_installed() == 0:
            if password_ubuntu_input:
                pass
            else:
                password_ubuntu_input = set_ubuntu_user_password()
            install_epics_base(password_ubuntu_input)
        else:
            print('Passed EPICS installed check')
            pass
    if checkbox_install_camels:
        if sanity_check_camels_installed(camels_install_path) == 0:
            install_camels()
        else:
            print('Passed CAMELS installed check')
            pass
    if checkbox_install_pythonenv:
        if sanity_check_pyenv_installed() == 0:
            install_pyenv()
            setup_python_environment()
        else:
            print('Passed pyenv installed check')
            setup_python_environment()

    run_camels()


if __name__ == '__main__':
    print(sys.argv[0])
    # full_sanity_check(os.path.expanduser('~'))
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = InstallerWindow()
    ui.show()
    app.exec_()

    