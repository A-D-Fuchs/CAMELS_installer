import codecs
import os
import re
import subprocess
import sys


def check_if_pyenv_installed():
    """
    Checks to see if pyenv is already installed.
    Pyenv is used to set up a clean python environemnt for CAMELS.


    Returns
    -------
    True: if pyenv is installed\n
    False: if pyenv is not installed
    """
    if (subprocess.run(["powershell", "pyenv"],
                       stderr=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW, )).returncode == 0:
        print('pyenv already installed')
        return True
    elif (subprocess.run(["powershell", "pyenv"],
                         stderr=subprocess.PIPE,
                         creationflags=subprocess.CREATE_NO_WINDOW, )).returncode == 1:
        print('pyenv not installed')
        return False


def run_pyenv_install(temp_path):
    """
    Installs pyenv using a single powershell script.
    Uninstall with following command in command line: 'install-pyenv-win.ps1 -uninstall'

    :param temp_path: path to a temporary folder in {tmp} created by Inno Setup when installing
    :return: None
    """
    subprocess.run(['powershell', f'cd {temp_path};Invoke-WebRequest -UseBasicParsing -Uri '
                                  '"https://raw.githubusercontent.com/pyenv-win/pyenv'
                                  '-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile '
                                  '"./install-pyenv-win.ps1"; '
                                  '&"./install-pyenv-win.ps1";Remove-Item '
                                  './install-pyenv-win.ps1 '],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def check_pyenv_version(folder_path, ):
    ret = subprocess.run(['powershell', f'cd {folder_path};pyenv --version'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         creationflags=subprocess.CREATE_NO_WINDOW, ).stdout.decode('utf-8')
    search = re.search(r'pyenv\s(\d.\d.?\d?)', ret)
    version = search.group(1)
    if version:
        return version
    else:
        raise ValueError('pyenv installation seems to have failed as no valid pyenv version '
                         'can be read')


def install_python_version(python_version):
    subprocess.run(['powershell', f'pyenv install {python_version}'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def set_local_python_version(nomad_camels_install_path, python_version):
    if os.path.isdir(nomad_camels_install_path):
        pass
    else:
        raise OSError(f'Could not find the CAMELS folder: {nomad_camels_install_path}')
    subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                  f'pyenv local {python_version}'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def create_desertenv(nomad_camels_install_path):
    python_exe_path = subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                                    'pyenv which python'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, ).stdout.decode('utf-8').replace(
        '\r\n', '')
    subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                  f'{python_exe_path} -m venv .desertenv;'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def pip_install_camels(nomad_camels_install_path):
    pip_exe_path = subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                                 'pyenv which pip'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, ).stdout.decode('utf-8').replace(
        '\r\n', '')
    subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                  r'.\.desertenv\Scripts\activate;'
                                  f'pip install '
                                  'git+https://github.com/FAU-LAP/CAMELS.git'
                                  '@development'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def create_ini_file(nomad_camels_install_path=None):
    if os.path.exists(
            os.path.join(nomad_camels_install_path, r'.desertenv\Scripts\pythonw.exe')):
        python_exe_path = os.path.join(nomad_camels_install_path,
                                       r'.desertenv\Scripts\pythonw.exe')
        # python_exe_path = subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
        #                                                 'pyenv which python'],
        #                                  stdout=subprocess.PIPE,
        #                                  stderr=subprocess.PIPE, ).stdout.decode(
        #     'utf-8').replace(
        #     '\r\n', '')
    if os.path.exists(os.path.join(nomad_camels_install_path,
                                   r'.desertenv\Lib\site-packages\CAMELS\CAMELS_start.py')):
        camels_start_path = os.path.join(nomad_camels_install_path,
                                         r'.desertenv\Lib\site-packages\CAMELS\CAMELS_start.py')
    subprocess.run(['powershell', f'cd {nomad_camels_install_path};'
                                  fr'New-Item -Path .\run\ '
                                  '-Name "CAMELS.ini" -ItemType "file" -Value '
                                  f'@"\npython_exe_path={python_exe_path}\n'
                                  f'camels_start_path={camels_start_path}\n"@\n;'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )


def main_setup_python_environment(nomad_camels_install_path=None,
                                  temp_path=None):
    """
    Installs the correct python version (3.9.6) using pyenv and then sets up the environment
    '.desertenv' in the NOMAD_CAMELS folder created by the Inno Setup installer.

    Returns
    -------
    """
    python_version = '3.9.6'
    if check_if_pyenv_installed():
        print('pyenv is already installed')
        pyenv_version = check_pyenv_version(
            nomad_camels_install_path)  # more for debugging purposes
    else:
        print('pyenv not installed')
        run_pyenv_install(temp_path)
        pyenv_version = check_pyenv_version(
            nomad_camels_install_path)  # more for debugging purposes
    print('install_python_version')
    install_python_version(python_version)
    print('set_local_python_version')
    set_local_python_version(nomad_camels_install_path, python_version)
    print('create_desertenv')
    create_desertenv(nomad_camels_install_path)
    print('pip_install_camels')
    pip_install_camels(nomad_camels_install_path)
    print('create_ini_file')
    create_ini_file(nomad_camels_install_path)


if __name__ == '__main__':
    temp_path_ = r'C:\Users\yh43epyd\AppData\Local\Temp\junk_tmp'
    nomad_camels_install_path_ = r'C:\EAGLE-7.7.0\NOMAD-CAMELS'
    if len(sys.argv) > 1:
        nomad_camels_install_path_ = sys.argv[1]
        temp_path_ = sys.argv[2]
    main_setup_python_environment(nomad_camels_install_path=nomad_camels_install_path_,
                                  temp_path=temp_path_)
