import os
import re
import subprocess
import sys
import time
import tkinter.simpledialog
import tkinter.messagebox


def sanity_check_wsl_enabled(info_signal=None):
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
                                      creationflags=subprocess.CREATE_NO_WINDOW,
                                    #  encoding='utf-16le',
                                      )).stdout
    wsl_help_output = wsl_help_output.decode('utf-16')
    if info_signal:
        if '--set-default' in wsl_help_output:
            info_signal.emit('WSL is enabled')
            enabled = 1
        else:
            info_signal.emit('WSL not enabled')
            enabled = 0
        return enabled
    else:
        if '--set-default' in wsl_help_output:
            enabled = 1
        else:
            enabled = 0
        return enabled
        

def sanity_check_ubuntu_installed(info_signal=None):
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
    wsls = (subprocess.run(["powershell", "wsl", " -l", " -q"],
                           #encoding='utf-16le',
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE, shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW,)).stdout
    wsls = wsls.decode('utf-16')
    if info_signal:
        if re.search(ubuntu_regex, wsls) is None:
            info_signal.emit('Ubuntu is not installed.')
            installed = 0
        else:
            info_signal.emit('Ubuntu is already installed.')
            installed = 1
        return installed
    else:
        if re.search(ubuntu_regex, wsls) is None:
            installed = 0
        else:
            installed = 1
        return installed


def sanity_check_ubuntu_user_exists(info_signal=None):
    """
    Sanity check to see if the user 'epics' already exists in the Ubuntu environment.

    Returns
    -------
    1: if 'epics' is the default user\n
    0: if 'epics' is not the default user'

    """
    default_user = str((subprocess.run(["powershell", "wsl", " whoami"],
                        encoding='utf-8',
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE, shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW, )).stdout)
    if default_user == 'epics\n':
        if info_signal:
            info_signal.emit("User 'epics' is already setup.")
        return (1)
    else:
        if info_signal:
            info_signal.emit("A different user than 'epics' is setup as default")
            info_signal.emit("Enter a password for the current default Ubuntu user:")
        return (0)



def sanity_check_epics_installed(info_signal=None):
     """
     Sanity check to see if EPICS is already installed on the computer. 
     Searches for the EPICS folder in the WSLS /home/user directory.
     
     Returns
     -------
     1: if EPICS is already installed\n
     0: if EPICS is not installed
     
     """ 
     if info_signal:
         if 'EPICS' in ((subprocess.run(['powershell','wsl','ls /home/epics'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE, shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,)).stdout).decode('utf-8'):
             info_signal.emit('EPICS installed already.')
             installed = 1
         else:
             info_signal.emit('EPICS not installed yet.')
             installed = 0
         return installed
     else:
         if 'EPICS' in ((subprocess.run(['powershell','wsl','ls /home/epics'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE, shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,)).stdout).decode('utf-8'):
             installed = 1
         else:
             installed = 0
         return installed

      
def sanity_check_camels_installed(camels_install_path,info_signal):
    """
    Sanity check to see if CAMELS is already installed in the path 
    given in the installer. 
    
    
    Returns
    -------
    1: if a CAMELS folder is already exists in path\n
    0: if CAMELS folder does not exists in path
    
    """
    if os.path.exists(os.path.join(f'{camels_install_path}', "CAMELS")):
        info_signal.emit('CAMELS folder already exists. CAMELS seems to be installed already.')
        installed = 1
    else:
        info_signal.emit('CAMELS folder does not exists yet.')
        installed = 0
    return installed

def sanity_check_pyenv_installed(info_signal):
    """
    Sanity check to see if pyenv is already installed on the windows computer. 
    Pyenv is used to setup a clean python environemnt for CAMELS.
    
    
    Returns
    -------
    1: if pyenv is installed\n
    0: if pyenv is not installed
    
    """
    if (subprocess.run(["powershell", "pyenv"],                  
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)).returncode == 0:
        info_signal.emit('pyenv already installed')
        installed = 1
    elif (subprocess.run(["powershell", "pyenv"],                  
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)).returncode == 1:
        info_signal.emit('pyenv not installed')
        installed = 0
    return installed   
    

def enable_wsl(exe_path,checkbox_install_wsl, checkbox_install_epics,
               checkbox_install_camels, checkbox_install_pythonenv, camels_install_path):
    path_of_exe = sys.argv[0]
    path_exe_location = os.path.dirname(path_of_exe)
    if checkbox_install_wsl:
        checkbox_install_wsl = 'wsl'
    if checkbox_install_epics:
        checkbox_install_epics = 'epics'
    if checkbox_install_camels:
        checkbox_install_camels = 'camels'
    if checkbox_install_pythonenv:
        checkbox_install_pythonenv = 'pythonenv'
    startup_path = os.path.join(os.path.expanduser('~'), r"AppData\Roaming\Microsoft\Windows\Start "
                                  r"Menu\Programs\Startup\camels_restart.lnk")
    subprocess.run(['powershell', f'$SourceFilePath = "{path_of_exe}";'
    rf'$ShortcutPath = "{startup_path}";'
    r'$WScriptObj = New-Object -ComObject ("WScript.Shell");'
    r'$shortcut = $WscriptObj.CreateShortcut($ShortcutPath);'
    r'$shortcut.TargetPath = $SourceFilePath;'
    f'$shortcut.Arguments = "{checkbox_install_wsl} {checkbox_install_epics} '
    f'{checkbox_install_camels} {checkbox_install_pythonenv} {camels_install_path}";'
    f'$shortcut.WorkingDirectory = "{path_exe_location}";'
    r'$shortcut.Save();'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    subprocess.run(["powershell", "Start-Process", "powershell",
                    r"'dism.exe /online /enable-feature "
                    r"/featurename:Microsoft-Windows-Subsystem-Linux "
                    r"/all /norestart'", "-Verb", "runAs"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    time.sleep(3)
    restart_windows_answer = tkinter.messagebox.askquestion(
        'Restart Windows', 'Klick Yes to restart Windows now and '
                           'to continue the installation')
    if restart_windows_answer == 'yes':
        subprocess.run(["powershell", "Restart-Computer -Force"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.PIPE, shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW,)

    


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


def input_password_once():
    tkinter.Tk().withdraw()
    password_ubuntu_input = tkinter.simpledialog.askstring("Password",
                                                           "Enter password for the current "
                                                           "default Ubuntu user: \n"
                                                           "This user must have sudo rights!",
                                                           show='*')
    return password_ubuntu_input


def ubuntu_installer(password_ubuntu_input, info_signal):
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
    info_signal.emit('Setting default WSL version to 1')
    subprocess.run(["powershell", "wsl --set-default-version 1"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Installing Ubuntu')
    info_signal.emit('Do NOT close the Ubuntu terminal until it asks you for a username and password!')
    info_signal.emit('Close the Ubuntu terminal after it asks you for a username and password')
    info_signal.emit('Wait for a Ubuntu command prompt to open.')
    subprocess.run(["powershell", "wsl --install -d Ubuntu"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Installing Ubuntu.  Only click Yes after it asks you for a username and password ')
    # Here we would wait for a button to be pressed or something to continue
    ##############
    tkinter.Tk().withdraw()
    ubuntu_installed_question = tkinter.messagebox.askquestion(
        'Ubuntu installed?', 'Klick Yes when Ubuntu is successfully installed')
    if ubuntu_installed_question == 'yes':
        subprocess.run(['powershell','taskkill /IM ubuntu.exe /F'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW,)
    ##############
    wsls = (subprocess.run(["powershell", "wsl -l -q"],
                           #encoding='utf-16le',
                           capture_output=True, shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW,)).stdout
    wsls = wsls.decode('utf-16')
    ubuntu_regex_match = re.search(ubuntu_regex, wsls)
    subprocess.run(["powershell", f"wsl --setdefault {ubuntu_regex_match.group(1)}"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    # sets the root password to root
    subprocess.run(["powershell","wsl", "chpasswd `<`<`< root:root"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('Running regex match for user name')
    get_epics_user_id = ((subprocess.run(['powershell',"wsl", "id", "-u", "epics"],
                                                    # encoding=' utf-8',
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.PIPE,
                                                      stdin=subprocess.PIPE,
                                         creationflags=subprocess.CREATE_NO_WINDOW,)).stderr)
    get_epics_user_id = get_epics_user_id.decode('utf-8')
    if re.search('.*no such user.*', get_epics_user_id):
        info_signal.emit('creating user: "epics" in fresh install')
        info_signal.emit(r'Adding user')
        subprocess.run(['powershell',"wsl", "adduser", "epics"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW,)
        info_signal.emit('Changing password')
        subprocess.run(["powershell","wsl","chpasswd `<`<`<" f"epics:{password_ubuntu_input}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW,
                       )
        info_signal.emit('Adding user to sudo group')
        subprocess.run(['powershell',"wsl", "sudo", "usermod", "-aG", "sudo", "epics"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW,)
        info_signal.emit('Setting user as default')
        subprocess.run(["powershell", "ubuntu config --default-user epics"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                       stdin=subprocess.PIPE,
                       shell=True, creationflags=subprocess.CREATE_NO_WINDOW, )


def set_ubuntu_user_password(info_signal):
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
            password_ubuntu_input = input_password()

    if password_ubuntu_input is None:
        password_ubuntu_input = f'{default_ubuntu_password}'
        info_signal.emit(f'Your password was set to \'{default_ubuntu_password}\' '
                         f'as none was given')
        tkinter.messagebox.showinfo('Force Password',
                                    'Password set to epics4camels '
                                    'as no valid password was given')
    else:
        if len(password_ubuntu_input) == 0:
            password_ubuntu_input = f'{default_ubuntu_password}'
            info_signal.emit(f'Your password was set to \'{default_ubuntu_password}\' '
                             f'as none was given')
            tkinter.messagebox.showinfo('Force Password',
                                        'Password set to epics4camels '
                                        'as no valid password was given')

    info_signal.emit('Setting password was successful')
    return password_ubuntu_input


def input_ubuntu_user_password(info_signal=None):
    """
    This function asks the user to input the password for the already existing Ubuntu user.
    Not typing a password and pressing 'OK' or clicking 'Cancel'  will cause another
    password input prompt.
    """
    tkinter.Tk().withdraw()
    password_ubuntu_input = input_password_once()

    if password_ubuntu_input is None:
        tkinter.messagebox.showinfo("Invalid password - Password is None",
                                    "Please enter a valid password "
                                    "for the default WSL user")
        password_ubuntu_input = input_password_once()
    if info_signal:
        info_signal.emit('Setting password was successful')
    # tkinter.messagebox.showinfo('Setting password successful',
    #                             'Password set. Click OK to continue and install Ubuntu')
    return password_ubuntu_input

def setup_epics_user(default_user_password, ubuntu_pwd, info_signal):
    """
    :param default_user_password: Password of the currently installed default Ubuntu user
    with sudo rights
    :param ubuntu_pwd: Password that should be used for the Ubuntu user 'epics'
    :param info_signal:
    :return:
    """
    ubuntu_regex = r"(u*U*buntu\w{0,3}\.{0,1}\w{0,3})\n*"
    wsls = (subprocess.run(["powershell", "wsl -l -q"],
                           # encoding='utf-16le',
                           capture_output=True, shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, )).stdout
    wsls = wsls.decode('utf-16')
    ubuntu_regex_match = re.search(ubuntu_regex, wsls)
    info_signal.emit('setting Ubuntu as the default WSL')
    subprocess.run(["powershell", f"wsl --setdefault {ubuntu_regex_match.group(1)}"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW, )
    info_signal.emit('creating user: "epics" in existing install')
    info_signal.emit(r'Adding user')
    subprocess.run(
        ["wsl", "sudo", "-S", "<<<", f"{default_user_password}", "adduser", "epics",
         "&&", "sudo", "chpasswd", "<<<", f"epics:{ubuntu_pwd}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW, )
    info_signal.emit('Adding user to sudo group')
    subprocess.run(["wsl","sudo", "-S", "<<<", f"{default_user_password}", "usermod", "-aG", "sudo", "epics"],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW, )
    info_signal.emit('Setting user as default')
    subprocess.run(["powershell", "ubuntu config --default-user epics"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW, )



def install_epics_base(password_ubuntu_input,info_signal,):
    """
    This function installs a basic version of EPICS in the Ubuntu WSL.
    It is derived from the debian-setup.py from the FHI Gitlab page
    https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup.

    Parameters
    ----------
    password_ubuntu_input: Password passed to this function by ubuntu_installer() and initially
    set by set_ubuntu_user_password().
    The default password if no password was given is 'epics4camels' without the parenthesis.

    -------

    """
    CORES = os.cpu_count()

    info_signal.emit('Updating apt')
    subprocess.run(['powershell',"wsl", "sudo", "-S", "`<`<`<", f"{password_ubuntu_input}", "apt", "update"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('Upgrading apt')
    subprocess.run(['powershell',"wsl", "sudo", "-S", "`<`<`<", f"{password_ubuntu_input}",
                    "apt", "dist-upgrade", "-y"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

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

    info_signal.emit('Installing required packages')
    for package in package_list:
        info_signal.emit(f'Installing relevant package: {package}')
        run = subprocess.run(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}",
                        "apt", "install", "-y", f"{package}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('Cloning EPICS-base to base-7.0')
    subprocess.run(["wsl", "git", "clone", "--recursive", "-b", "7.0",
                    "https://github.com/epics-base/epics-base", "/home/epics/EPICS/base-7.0"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('creating symbolic link from epics-base to base-7.0')
    subprocess.run(["wsl", "ln", "-s", "/home/epics/EPICS/base-7.0/",
                    "/home/epics/EPICS/epics-base"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('Make epics-base')
    subprocess.run(["wsl", "make", "-j", f"{CORES}", "-C", "/home/epics/EPICS/epics-base"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    wsl_path: str = os.path.join(r"\\wsl$\Ubuntu", '')
    info_signal.emit("setting up EPICS environment...")
    epics_env = ("\n\nexport EPICS_BASE=\${HOME}/EPICS/epics-base\n"
                     "export EPICS_HOST_ARCH=\$(\${EPICS_BASE}/startup/EpicsHostArch)\n"
                     "export PATH=\${EPICS_BASE}/bin/\${EPICS_HOST_ARCH}:\${PATH}\n"
                )
    content = str(subprocess.run(["wsl", "cd", "~","&&", "more", ".bashrc"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,).stdout)
    print(f'{content}')
    if ("export EPICS_BASE=${HOME}/EPICS/epics-base") in content:
        info_signal.emit('EPICS BASE already added to path')
    else:
        info_signal.emit('Setting EPICS environment variables in .bashrc')
        subprocess.run(["wsl", "cd", "~", "&&", "echo", "-e", f"{epics_env}", ">>", ".bashrc"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW, )

    info_signal.emit('Cloning support modules')
    subprocess.run(["wsl", "git", "clone", "--recursive",
                    "https://gitlab.fhi.mpg.de/junkes/epics-support",
                    "/home/epics/EPICS/epics-support"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Making support modules')
    subprocess.run(["wsl", "cd", "/home/epics/EPICS/epics-support", "&&",
                    "python3", "./BuildAll.py", "make"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)

    info_signal.emit('Create IOCs folder')
    try:
        subprocess.run(["wsl", "mkdir", "/home/epics/IOCs"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW,)
    except FileExistsError:
        info_signal.emit('IOCs folder exists')
        pass
    try:
        open(os.path.join(wsl_path, '/home/epics/EPICS/epics-support/RELEASE.local'))
    except:
        info_signal.emit("RELEASE.local not present, not linking.\n")
    try:
        (subprocess.run(["wsl", "ln", "-s", "/home/epics/EPICS/epics-support/RELEASE.local",
                         "/home/epics/IOCs/RELEASE.local"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW,))
        info_signal.emit("linked SUPPORT RELEASE.local into IOCs folder.\n")
    except:
        info_signal.emit("link or file already existing.\n")


def install_camels(info_signal):
    """
    Installs the actual CAMELS software. Installs pyenv and uses it to install a defined
    python version: currently 3.9.6.
    Then uses venv to create a specific python environment called .desertenv
    for which all required packages are installed using pip.


    Returns
    -------

    """
    info_signal.emit('Installing CAMELS')
    info_signal.emit('Cloning files from Github')

    subprocess.run(["powershell", "git clone https://github.com/FAU-LAP/CAMELS.git "
                                  "%USERPROFILE%/CAMELS"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW, )
    info_signal.emit('Installing module for PID controller')
    subprocess.run(["powershell", "wsl", "cd ~/EPICS/epics-support/ `&`& "
                                         "git clone https://github.com/epics-modules/std.git"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)


def install_pyenv(info_signal):
    info_signal.emit('Install pyenv')
    info_signal.emit('Setup correct line endings so that all are in UNIX format')
    subprocess.run(["powershell", "git config --global core.eol lf;git config --global core.autocrlf input"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Clone pyenv for windows from Github')
    subprocess.run(["powershell", "cd $HOME; git clone https://github.com/pyenv-win/pyenv-win.git"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    if not os.path.exists(os.path.join(os.path.expanduser('~'), "CAMELS")):
        info_signal.emit('Git clone unsuccessful.')
        git_install_test = (subprocess.run(['powershell', 'git help -a'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)).stdout
        if r"See 'git" not in git_install_test:
            info_signal.emit('Git does not seem to be installed. Please install!')
            time.sleep(10)
            sys.exit(1)

    info_signal.emit('Create .pyenv folder in the $HOME directory')
    info_signal.emit('Copy pyenv-win folder and .version file to .pyenv from the cloned folder')
    subprocess.run(["powershell", "mkdir $HOME/.pyenv; Copy-Item $HOME/pyenv-win/pyenv-win "
                                  "-Destination $HOME/.pyenv -Recurse; "
                                  "Copy-Item $HOME/pyenv-win/.version -Destination $HOME/.pyenv "],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Set environment variables')
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
    info_signal.emit('Set script execution policy to "unrestricted " for the current user')
    subprocess.run(["powershell", r'Set-ExecutionPolicy -ExecutionPolicy Unrestricted '
                                  r'-Scope CurrentUser -Force'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

    subprocess.run(["powershell", r'Unblock-File $HOME/.pyenv/pyenv-win/bin/pyenv.ps1'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)


def setup_python_environment(camels_install_path,info_signal):

    info_signal.emit('Installing python version 3.9.6')
    subprocess.run(["powershell", f"cd {os.path.expanduser('~')};"
                    "pyenv install 3.9.6"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    info_signal.emit('Setting python 3.9.6 as the default global python in Powershell')
    subprocess.run(["powershell", "pyenv global 3.9.6"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

    if '3.9.6' in (subprocess.run(["powershell", "pyenv versions"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                          shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)).stdout:
        info_signal.emit('Installed 3.9.6 successfully')
    else:
        info_signal.emit('Python 3.9.6 is not installed')

    #info_signal.emit('Creating python virtual environment .desertenv')
    subprocess.run(["powershell", fr"cd {camels_install_path}; python -m venv .desertenv"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)
    #info_signal.emit('Installing the required packages into the virtual environment')
    subprocess.run(["powershell", fr"cd {camels_install_path}; ./.desertenv/Scripts/activate; "
                                  fr"pip install -r {camels_install_path}/requirements.txt"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   creationflags=subprocess.CREATE_NO_WINDOW,)
    subprocess.run(['powershell',f'New-Item {camels_install_path}/runcamels.cmd;',
                    fr'Set-Content {camels_install_path}/runcamels.cmd "powershell cd {camels_install_path}/.desertenv/Scripts/; .\activate;cd {camels_install_path};pythonw MainApp.py"'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)


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
                   shell=True, creationflags=subprocess.CREATE_NO_WINDOW,)

