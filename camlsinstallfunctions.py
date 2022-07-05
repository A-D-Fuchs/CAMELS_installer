import os
import re
import subprocess
import sys
import tkinter.simpledialog
import tkinter.messagebox


def sanity_check_wsl_enabled():
    """
    Sanity check to see if the WSL is enabled for windows on the PC. 
    
    Returns
    -------
    1: if WSL is already enabled\n
    0: if WSL is not enabled
    
    """
    wsl_help_output = (subprocess.run(["powershell", "wsl", "--help"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      stdin=subprocess.PIPE,
                                      encoding='utf-16le',
                                      )).stdout

    if '--set-default' in wsl_help_output:
        print('WSL is enabled')
        enabled = 1
    else:
        print('WSL not enabled')
        enabled = 0
    return enabled
        

def sanity_check_ubuntu_installed():
    """
    Sanity check to see if Ubuntu is already installed on the computer. 
    Searches for any Ubuntu distro with r"(u*U*buntu\w{0,3}\.{0,1}\w{0,3})\n*"
    regex search.
    
    Returns
    -------
    1: if a Ubuntu is already installed\n
    0: if Ubuntu is not installed
    
    """
    ubuntu_regex = r"(u*U*buntu\w{0,3}\.{0,1}\w{0,3})\n*"
    wsls = (subprocess.run(["powershell", "wsl", " -l", " -q"], encoding='utf-16le',
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE, shell=True, text=True)).stdout
    if re.search(ubuntu_regex, wsls) is None:
        print('Ubuntu is not installed.')
        installed = 0
    else: 
        print('Ubuntu is already installed.')
        installed = 1
    return installed


def sanity_check_epics_installed():
     """
     Sanity check to see if EPICS is already installed on the computer. 
     Searches for the EPICS folder in the WSLS /home/user directory.
     
     Returns
     -------
     1: if EPICS is already installed\n
     0: if EPICS is not installed
     
     """ 
     if 'EPICS' in (subprocess.run([r'wsl','ls /home/epics'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE, shell=True, text=True)).stdout:
         print('EPICS installed already.')
         installed = 1
     else:
         print('EPICS not installed yet.')
         installed = 0
     return installed

      
def sanity_check_camels_installed(camels_install_path):
    """
    Sanity check to see if CAMELS is already installed in the path 
    given in the installer. 
    
    
    Returns
    -------
    1: if a CAMELS folder is already exists in path\n
    0: if CAMELS folder does not exists in path
    
    """
    if os.path.exists(os.path.join(f'{camels_install_path}', "CAMELS")):
        print('CAMELS folder already exists. CAMELS seems to be installed already.')
        installed = 1
    else:
        print('CAMELS folder does not exists yet.')
        installed = 0
    return installed

def sanity_check_pyenv_installed():
    """
    Sanity check to see if pyenv is already installed on the windows computer. 
    Pyenv is used to setup a clean python environemnt for CAMELS.
    
    
    Returns
    -------
    1: if pyenv is installed\n
    0: if pyenv is not installed
    
    """
    if (subprocess.run(["powershell", "pyenv"],                  
                   shell=True, text=True)).returncode == 0:
       print('pyenv already installed')
       installed = 1
    elif (subprocess.run(["powershell", "pyenv"],                  
                   shell=True, text=True)).returncode == 1:
       print('pyenv not installed')
       installed = 0
    return installed   
    


def enable_wsl():        
    subprocess.run(["powershell", "Start-Process", "powershell",
                    r"'dism.exe /online /enable-feature "
                    r"/featurename:Microsoft-Windows-Subsystem-Linux "
                    r"/all /norestart'", "-Verb", "runAs"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True, text=True)
    restart_windows_answer = tkinter.messagebox.askquestion(
        'Restart Windows', 'Klick Yes to restart Windows now and '
                           'to continue the installation')
    if restart_windows_answer == 'yes':
        subprocess.run(["powershell", "Restart-Computer -Force"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.PIPE, shell=True, text=True)

    


def input_password():
    tkinter.Tk().withdraw()
    password_ubuntu_input = tkinter.simpledialog.askstring("Password",
                                                           "Enter password for the Ubuntu user:",
                                                           show='*')
    password_ubuntu_input_repeat = tkinter.simpledialog.askstring("Password",
                                                                  "Repeat password for the Ubuntu user:",
                                                                  show='*')
    if password_ubuntu_input == password_ubuntu_input_repeat:
        pass
    else:
        tkinter.messagebox.showinfo('Error', 'Passwords not the same. Retry.')
        password_ubuntu_input = input_password()
    return password_ubuntu_input


def set_ubuntu_user_password():
    """
    This function asks the user to input the password for the Ubuntu user 'epics'.
    Not typing a password and pressing 'OK' or clicking 'Cancel'  will cause another
    password input prompt.
    It calls the Ubuntu setup function and passes the password to that function.
    """
    default_ubuntu_password = 'epics4camels'
    tkinter.Tk().withdraw()
    password_ubuntu_input = input_password()

    if password_ubuntu_input is None:
        tkinter.messagebox.showinfo("Invalid password - Password is None",
                                    "Please enter a valid password "
                                    "for the Ubuntu user")
        input_password()
    if password_ubuntu_input is not None:
        if len(password_ubuntu_input) == 0:
            tkinter.messagebox.showinfo("Invalid password", "Password must contain at "
                                                            "least 1 character")
            input_password()

    if password_ubuntu_input is None:
        password_ubuntu_input = f'{default_ubuntu_password}'
        print(f'Your password was set to \'{default_ubuntu_password}\' as none was given')
        tkinter.messagebox.showinfo('Force Password',
                                    'Password set to epics4camels '
                                    'as no valid password was given')
    else:
        if len(password_ubuntu_input) == 0:
            password_ubuntu_input = f'{default_ubuntu_password}'
            print(f'Your password was set to \'{default_ubuntu_password}\' as none was given')
            tkinter.messagebox.showinfo('Force Password',
                                        'Password set to epics4camels '
                                        'as no valid password was given')

    tkinter.messagebox.showinfo('Setting password successful',
                                'Password set. Click OK to continue and install Ubuntu')
    return password_ubuntu_input


def ubuntu_installer(password_ubuntu_input):
    """
    Performs a complete Ubuntu WSL install. First enables WSL on the Windows machine if
    it is not already enabled. This is done by checking the wsl --help command.
    Then 'wsl -l -q' is executed to see if an Ubuntu version is already installed on the system.
    If no Ubuntu distribution is found a new Ubuntu distro is installed.
    This opens a Ubuntu terminal. Do not close the terminal or Ubuntu will not install!
    The Ubuntu terminal can be closed when it asks you for a name and password.
    The password of root is set to root and a user named 'epics' is created and given the
    password passed to this function.

    !!!
    If there is already a sudo user as default and no epics user this should be created now
    BUT: This still needs to be done and is more involved!
    !!!

    Parameters
    ----------
    password_ubuntu_input: Password passed to this function by set_ubuntu_user_password().
    The default password if no password was given is 'epics4camels' without the paranthesis.

    -------

    """
    ubuntu_regex = r"(u*U*buntu\w{0,3}\.{0,1}\w{0,3})\n*"
    print('Setting default WSL version to 1')
    subprocess.run(["powershell", "wsl --set-default-version 1"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True, text=True)
    print('Installing Ubuntu')
    print('Do NOT close the Ubuntu terminal until it asks you for a username and password!')
    print('Close the Ubuntu terminal after it asks you for a username and password')
    print('Installing Ubuntu')
    subprocess.run(["powershell", "wsl --install -d Ubuntu"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True, text=True)
    # Here we would wait for a button to be pressed or something to continue
    ##############
    input("After the installation in the terminal window has finished: "
          "Press Enter to continue...")
    ##############
    wsls = (subprocess.run(["powershell", "wsl -l -q"], encoding='utf-16le',
                           capture_output=True, shell=True, text=True)).stdout
    ubuntu_regex_match = re.search(ubuntu_regex, wsls)
    subprocess.run(["powershell", f"wsl --setdefault {ubuntu_regex_match.group(1)}"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True, text=True)

    # sets the root password to root
    subprocess.run(["wsl", "echo", "root:root", "|", "chpasswd"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True, text=True)

    print('Running regex match for user name')
    if re.search('.*no such user.*', ((subprocess.run(["wsl", "id", "-u", "epics"],
                                                      text=True, encoding=' utf-8',
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.PIPE,
                                                      stdin=subprocess.PIPE)).stderr)):
        print('creating user: "epics" in fresh install')
        print(r'Adding user')
        subprocess.run(["wsl", "adduser", "epics"], text=True, 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print('Changing password')
        subprocess.run(["wsl", "echo", f"epics:{password_ubuntu_input}", 
                        "|", "chpasswd"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                       stdin=subprocess.PIPE,
                       text=True)
        print('Adding user to sudo group')
        subprocess.run(["wsl", "usermod", "-aG", "sudo", "epics"], 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        print('Setting user as default')
        subprocess.run(["powershell", "ubuntu config --default-user epics"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                       stdin=subprocess.PIPE,
                       shell=True, text=True)

    # if re.search('.*no such user.*', ((subprocess.run(["Ubuntu", "run", "id", "-u", "epics"],
    #                                                   text=True, encoding=' utf-8',
    #                                                   stdout=subprocess.PIPE,
    #                                                   stderr=subprocess.PIPE,
    #                                                   stdin=subprocess.PIPE)).stderr)):
    #     print('creating user: "epics" in existing install')
    #     print('Adding user')
    #     print(subprocess.run(["wsl", "adduser", "epics"], stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True))
    #     print('Changing password')
    #     print(subprocess.run(["wsl", "echo", f"epics:{password_ubuntu_input}", "|", "chpasswd"],
    #                          stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE,
    #                          stdin=subprocess.PIPE,
    #                          text=True))
    #     print('Adding user to sudo group')
    #     print(subprocess.run(["wsl", "usermod", "-aG", "sudo", "epics"],
    #                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                          stdin=subprocess.PIPE, text=True))
    #     print('Setting user as default')
    #     print(subprocess.run(["powershell", "ubuntu config --default-user epics"],
    #                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                          stdin=subprocess.PIPE, shell=True, text=True))
    


def install_epics_base(password_ubuntu_input):
    """
    This function installs a basic version of EPICS in the Ubuntu WSL.
    It is derived from the debian-setup.py from the FHI Gitlab page
    https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup.

    Parameters
    ----------
    password_ubuntu_input: Password passed to this function by ubuntu_installer() and initially
    set by set_ubuntu_user_password().
    The default password if no password was given is 'epics4camels' without the paranthesis.

    -------

    """
    CORES = os.cpu_count()

    print('Updating apt')
    subprocess.run(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}", "apt", "update"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('Upgrading apt')
    subprocess.run(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}",
                    "apt", "dist-upgrade", "-y"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    # Removed iptables and iptables-persistent as manual input was required for the install
    # and broke the installer
    package_list = [
        "sudo",
        "git",
        "build-essential",
        "libreadline-dev",
        "dnsmasq",
        "dnsutils",
        "libtelnet2",
        "socat",
        "autoconf",
        "bison",
        "re2c",
        "libpcre3",
        "libpcre3-dev",
        "python3-setuptools"
    ]
    # package_list = ' '.join(package_list)

    print('Installing required packages')
    for package in package_list:
        print(f'    {package}')
        subprocess.run(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}",
                        "apt", "install", "-y", f"{package}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('Cloning EPICS-base to base-7.0')
    subprocess.run(["wsl", "git", "clone", "--recursive", "-b", "7.0",
                    "https://github.com/epics-base/epics-base", "/home/epics/EPICS/base-7.0"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('creating symbolic link from epics-base to base-7.0')
    subprocess.run(["wsl", "ln", "-s", "/home/epics/EPICS/base-7.0/",
                    "/home/epics/EPICS/epics-base"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('Make epics-base')
    subprocess.run(["wsl", "make", "-j", f"{CORES}", "-C", "/home/epics/EPICS/epics-base"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    wsl_path: str = os.path.join(r"\\wsl$\Ubuntu", '')
    print("setting up EPICS environment...")
    with open(os.path.join(wsl_path, '\home\epics\.bashrc'), "rb+") as profile:
        epics_env = ("\n\nexport EPICS_BASE=${HOME}/EPICS/epics-base\nexport "
        "EPICS_HOST_ARCH=$(${EPICS_BASE}/startup/EpicsHostArch)\nexport "
        "PATH=${EPICS_BASE}/bin/${EPICS_HOST_A}RCH}:${PATH}\n")
        content = profile.read()
        if ("EPICS_BASE").encode('UTF-8') in content:
            print('EPICS BASE already added to path')
        else:
            print('Setting EPICS environment variables in .bashrc')
            profile.write(epics_env.encode('UTF-8'))
            profile.truncate()

    print('Cloning support modules')
    subprocess.run(["wsl", "git", "clone", "--recursive",
                    "https://gitlab.fhi.mpg.de/junkes/epics-support",
                    "/home/epics/EPICS/epics-support"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print('Making support modules')
    subprocess.run(["wsl", "cd", "/home/epics/EPICS/epics-support", "&&",
                    "python3", "./BuildAll.py", "make"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('Create IOCs folder')
    try:
        subprocess.run(["wsl", "mkdir", "/home/epics/IOCs"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    except FileExistsError:
        print('IOCs folder exists')
        pass
    try:
        open(os.path.join(wsl_path, '/home/epics/EPICS/epics-support/RELEASE.local'))
    except:
        print("RELEASE.local not present, not linking.\n")
    try:
        (subprocess.run(["wsl", "ln", "-s", "/home/epics/EPICS/epics-support/RELEASE.local",
                         "/home/epics/IOCs/RELEASE.local"],
                        text=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, stdin=subprocess.PIPE))
        print("linked SUPPORT RELEASE.local into IOCs folder.\n")
    except:
        print("link or file already existing.\n")
    install_camels()


def install_camels():
    """
    Installs the actual CAMELS software. Installs pyenv and uses it to install a defined
    python version: currently 3.9.6.
    Then uses venv to create a specific python environment called .desertenv
    for which all required packages are installed using pip.


    Returns
    -------

    """
    print('Installing CAMELS')
    print('Cloning files from Github')

    subprocess.run(["powershell", "git clone https://github.com/FAU-LAP/CAMELS.git "
                                  "%USERPROFILE%/CAMELS"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Installing module for PID controller')
    subprocess.run(["powershell", "wsl", "cd ~/EPICS/epics-support/ `&`& "
                                         "git clone https://github.com/epics-modules/std.git"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)


def install_pyenv():
    print('Install pyenv')
    print('Setup correct line endings so that all are in UNIX format')
    subprocess.run(["powershell", "git config --global core.eol lf;git config --global core.autocrlf input"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Clone pyenv for windows from Github')
    subprocess.run(["powershell", "cd $HOME; git clone https://github.com/pyenv-win/pyenv-win.git"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    if not os.path.exists(os.path.join(os.path.expanduser('~'), "CAMELS")):
        print('Git clone unsuccessful.')
        git_install_test = (subprocess.run(['powershell', 'git help -a'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       shell=True, text=True)).stdout
        if r"See 'git" not in git_install_test:
            print('Git does not seem to be installed. Please install!')
            sys.exit(1)

    print('Create .pyenv folder in the $HOME directory')
    print('Copy pyenv-win folder and .version file to .pyenv from the cloned folder')
    subprocess.run(["powershell", "mkdir $HOME/.pyenv; Copy-Item $HOME/pyenv-win/pyenv-win "
                                  "-Destination $HOME/.pyenv -Recurse; "
                                  "Copy-Item $HOME/pyenv-win/.version -Destination $HOME/.pyenv "],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Set environemnt variables')
    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("PYENV",'
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\","User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)

    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("PYENV_HOME",'
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\","User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)

    subprocess.run(["powershell", r'[System.Environment]::SetEnvironmentVariable("path", '
                                  r'$env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE +'
                                  r' "\.pyenv\pyenv-win\shims;" + [System.Environment]::'
                                  r'GetEnvironmentVariable("path", "User"),"User")'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Set script execution policy to "unrestricted " for the current user')
    subprocess.run(["powershell", r'Set-ExecutionPolicy -ExecutionPolicy Unrestricted '
                                  r'-Scope CurrentUser -Force'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)

    subprocess.run(["powershell", r'Unblock-File $HOME/.pyenv/pyenv-win/bin/pyenv.ps1'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)


def setup_python_environment():

    print('Installing python version 3.9.6')
    subprocess.run(["powershell", f"cd {os.path.expanduser('~')};"
                    "pyenv install 3.9.6"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Setting python 3.9.6 as the default global python in Powershell')
    subprocess.run(["powershell", "pyenv global 3.9.6"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)

    if '3.9.6' in (subprocess.run(["powershell", "pyenv versions"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                          shell=True, text=True)).stdout:
        print('Installed 3.9.6 successfully')
    else:
        print('Install of Python 3.9.6 not successful')

    print('Creating python virtual environment .desertenv')
    subprocess.run(["powershell", r"cd $HOME/CAMELS; python -m venv .desertenv"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)
    print('Installing the required packages into the virtual environment')
    subprocess.run(["powershell", r"cd $HOME/CAMELS; ./.desertenv/Scripts/activate; "
                                  r"pip install -r $HOME/CAMELS/requirements.txt"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)


def run_camels():
    """
    Starts the CAMELS software by activating the virtual environment and running the MainApp.py
    from the $HOME/CAMELS/ folder.

    Returns
    -------

    """
    subprocess.run(["powershell", 'cd $HOME/CAMELS; '
                                  './.desertenv/Scripts/activate; '
                                  'python .\MainApp.py'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, text=True)

