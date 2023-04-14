# CAMELS_installer
Installs CAMELS software and all required packages

The relevant installer [NOMAD-CAMELS_installer.exe](/Output/NOMAD-CAMELS_installer.exe) 
file is located in [Output](/Output/)

Visit the [CAMELS Homepage](https://fau-lap.github.io/CAMELS/) for more information

## 1. Workflow
Brief description of the workflow when the installer should be updated.
### 1.1. Changes to python or environment
If you want to perform changed regarding the NOMAD-CAMELS version that is installed or 
changes to pyenv (python version) or the python environment then you have to perform 
changes in the python code of the [setup.py](/Python_code/setup_camels.py) file. Here the python version is currently hard-coded as `3.9.6`. The `pip install` command uses the most current version of NOMAD-CAMELS and ignores locally available versions with `--no-cache-dir`.
### 1.2. Changes to the way CAMELS is started (via shortcuts)
If you want to change the way CAMELS is startet you must modify the installation.exe file by modifying the InnoSetup file `.iss`. Here you can alter the shortcuts under `[Icons]`. 
The shortcuts simply execute the NOMAD-CAMELS.exe which is a simple exe convertion of the batch file `runCamels.bat`. This simply reads  the `NOMAD-CAMELS.ini` and read the paths to the exe and the installation path from it. You can change these two paths manually to change the python environment that should start CAMELS. 
