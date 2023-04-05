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
    1: if pyenv is installed\n
    0: if pyenv is not installed
    """
    if (subprocess.run(["powershell", "pyenv"],
                       creationflags=subprocess.CREATE_NO_WINDOW,)).returncode == 0:
        print('pyenv already installed')
        installed = 1
    elif (subprocess.run(["powershell", "pyenv"],
                         creationflags=subprocess.CREATE_NO_WINDOW,)).returncode == 1:
        print('pyenv not installed')
        installed = 0
    return installed

def install_pyenv(nomad_camels_folder_path,git_folder_path,):
    """
    Installs the correct python version (3.9.6) using pyenv and then sets up the environment
    '.desertenv' in the NOMAD_CAMELS folder.
    For this it uses a temporary git folder (created by the installer) to have access to the
    git command.


    Returns
    -------
    1: if pyenv is installed\n
    0: if pyenv is not installed
    """
    print('Install pyenv')
    print('Get current git settings')
    xx = subprocess.run(["powershell", "git config --list"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, ).stdout.decode('utf-8')
    print('Setup correct line endings so that all are in UNIX format')
    subprocess.run(["powershell", "git config --global core.eol lf;git config --global core.autocrlf input"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    print('Clone pyenv for windows from Github')
    subprocess.run(["powershell", "cd $HOME; git clone https://github.com/pyenv-win/pyenv-win.git"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    if not os.path.exists(os.path.join(os.path.expanduser('~'), "CAMELS")):
        print('Git clone unsuccessful.')
        git_install_test = (subprocess.run(['powershell', 'git help -a'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)).stdout
        if r"See 'git" not in git_install_test:
            print('Git does not seem to be installed. Please install!')
            sys.exit(1)

    print('Create .pyenv folder in the $HOME directory')
    print('Copy pyenv-win folder and .version file to .pyenv from the cloned folder')
    subprocess.run(["powershell", "mkdir $HOME/.pyenv; Copy-Item $HOME/pyenv-win/pyenv-win "
                                  "-Destination $HOME/.pyenv -Recurse; "
                                  "Copy-Item $HOME/pyenv-win/.version -Destination $HOME/.pyenv "],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    print('Set environment variables')
    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("PYENV",'
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\","User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("PYENV_HOME",'
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\","User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("path", '
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE +'
                                  r' "\.pyenv\pyenv-win\shims;" + [System.Environment]::'
                                  r'GetEnvironmentVariable("path", "User"),"User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    print('Set script execution policy to "unrestricted " for the current user')
    subprocess.run(["powershell", r'Set-ExecutionPolicy -ExecutionPolicy Unrestricted '
                                  r'-Scope CurrentUser -Force'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

    subprocess.run(["powershell", r'Unblock-File $HOME/.pyenv/pyenv-win/bin/pyenv.ps1'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)



if __name__ == '__main__':
    for i in sys.argv:
        print(i)
