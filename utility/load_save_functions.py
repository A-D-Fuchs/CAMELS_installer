import os.path
from os.path import isdir
from os import makedirs, getenv, listdir
from shutil import copyfile
import importlib

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QComboBox, QLineEdit, QWidget, QSplitter, QLabel,\
    QPushButton, QTreeView, QListView, QMenuBar, QAction, QMenu, QStatusBar,\
    QGridLayout

from datetime import datetime
import json
import ophyd

from main_classes import protocol_class
from utility.load_save_helper_functions import load_plots

appdata_path = f'{getenv("LOCALAPPDATA")}/CAMELS'
if not isdir(appdata_path):
    makedirs(appdata_path)
preset_path = f'{appdata_path}/Presets/'
backup_path = f'{preset_path}Backup/'
save_string_list = [QComboBox, QLineEdit, QTreeView, QListView]
save_dict_skip = [QWidget, QSplitter, QLabel, QPushButton, QMenu, QMenuBar,
                  QAction, QStatusBar, QGridLayout]


standard_pref = {'autosave': True,
                 'dark_mode': False,
                 'n_decimals': 3,
                 'number_format': 'mixed',
                 'mixed_from': 3,
                 'py_files_path': f'{appdata_path}/python_files'.replace('\\','/'),
                 'meas_files_path': os.path.expanduser('~/CAMELS_data').replace('\\','/'),
                 'device_driver_path': os.path.join(os.getcwd(), 'devices', 'devices_drivers').replace('\\','/'),
                 'autostart_ioc': True}

def get_preset_list():
    """returns a two list of available presets, once for devices, once
    for measurements. (files with ".predev" or ".premeas" in
    appdata_path. If the directory does not exist, it is created."""
    if isdir(preset_path):
        names = listdir(preset_path)
        if 'Backup' not in names:
            makedirs(preset_path + 'Backup')
        presets = []
        for name in names:
            if name.endswith('.preset'):
                presets.append(name[:-7])
        return sorted(presets, key=lambda x: x.lower())
    else:
        makedirs(preset_path)
        return get_preset_list()

def autosave_preset(preset:str, preset_data):
    """Saves the given preset and makes a backup of the former one in
    the backup-folder.

    Parameters
    ----------
    preset : str
        name of the preset to save
    preset_data : dict
        all the data contained in the preset
        (usually the __save_dict__ of the MainApp)
    """
    preset_file = f'{preset}.preset'
    with open(f'{preset_path}{preset_file}', 'w') as json_file:
        json.dump(preset_data, json_file, indent=2)
    make_backup(preset_file)

def save_preset(path:str, preset_data:dict):
    """Saves the given preset_data under the specified path.
    If the path ends with '.predev', the following autosave_preset of
    the saved data will be called with devices=True, otherwise
    devices=False."""
    preset_name = path.split('/')[-1][:-7]
    with open(path, 'w') as json_file:
        json.dump(preset_data, json_file, indent=2)
    autosave_preset(preset_name, preset_data)

def save_dictionary(path:str, dictionary:dict):
    """Saves the given `dictionary` as json to the given `path`."""
    save_dict = {}
    for key, val in dictionary.items():
        add_string = get_save_str(val)
        if add_string is not None:
            save_dict[key] = add_string
    with open(path, 'w') as file:
        json.dump(save_dict, file, indent=2)

def make_backup(preset_file:str):
    """Puts a copy of the given preset_file into the backup-folder of
    the preset. The current datetime is added to the filename."""
    backup_save_path = f'{backup_path}{preset_file[:-7]}/'
    if not isdir(backup_save_path):
        makedirs(backup_save_path)
    now = datetime.now()
    backup_name = f'{backup_save_path}{now.strftime("%Y-%m-%d_%H-%M-%S")}_{preset_file}'
    copyfile(f'{preset_path}{preset_file}', backup_name)

def load_save_dict(string_dict:dict, object_dict:dict, update_missing_key=False, remove_extra_key=False):
    """For all keys both given dictionaries have in common, the value of
    the object in object_dict will be updated to the corresponding value
    of the string in string_dict.

    Parameters
    ----------
    string_dict : dict
        dictionary with strings that should become the new values.
    object_dict : dict
        dictionary with the objects that should be updated.
    update_missing_key : bool, default False
        if True, keys that are in string_dict will be added to the
        object_dict, even if they are not there beforehand
    remove_extra_key : bool, default False
        if a key is in object_dict but not in string_dict, it is removed
    """
    for key in string_dict:
        if key in object_dict:
            obj = object_dict[key]
            val = string_dict[key]
            if issubclass(type(obj), QComboBox):
                obj.setCurrentText(val)
            elif issubclass(type(obj), QLineEdit):
                obj.setText(val)
            elif key == 'protocols_dict':
                load_protocols_dict(val, obj)
            elif key == 'active_devices_dict':
                load_devices_dict(val, obj)
            elif hasattr(obj, '__save_dict__') or hasattr(obj, '__dict__'):
                load_save_dict(val, obj.__dict__)
            elif type(obj) is dict:
                load_save_dict(val, obj, True, True)
            elif type(obj) is list:
                obj.clear()
                for v in val:
                    obj.append(v)
        elif update_missing_key:
            object_dict.update({key: string_dict[key]})
    if remove_extra_key:
        rem_keys = []
        for key in object_dict:
            if key not in string_dict:
                rem_keys.append(key)
        for key in rem_keys:
            object_dict.pop(key)

def get_save_str(obj):
    """Utility function to create the string with which to save the
    object-data.
    If the object has the attribute __save_dict__, it is the return value.
    Objects of the types specified in save_dict_skip return None.
    QComboBox and QLineEdit return their current text.
    If None of the above, an object with the attribute __dict__ will
    return that, otherwise the string of obj is returned."""
    if hasattr(obj, '__save_dict__'):
        make_save_dict(obj)
        return obj.__save_dict__
    if type(obj) in save_dict_skip:
        return None
    if isinstance(obj, ophyd.Device):
        return None
    if type(obj) in save_string_list:
        if issubclass(type(obj), QComboBox):
            return obj.currentText()
        if issubclass(type(obj), QLineEdit):
            return obj.text()
        return None
    if type(obj) is pd.DataFrame:
        obj.to_dict('list')
    if hasattr(obj, '__dict__') or type(obj) is dict:
        savedic = {}
        if hasattr(obj, '__dict__'):
            dictionary = obj.__dict__
        else:
            dictionary = obj
        for key in dictionary:
            if key == 'py_package':
                continue
            savedic.update({key: get_save_str(dictionary[key])})
        return savedic
    if type(obj) in [int, float, bool, np.float64]:
        return obj
    if type(obj) is np.ndarray:
        obj = list(obj)
    if type(obj) is list:
        obj_list = []
        for p in obj:
            obj_list.append(get_save_str(p))
        return obj_list
    return str(obj)

def make_save_dict(obj):
    """Utility function to update the __save_dict__ of the given obj.
    Goes through all the keys in __dict__ and calls get_save_str on the
    object. Thus working recursively if an attribute of obj also has a
    __save_dict__"""
    for key in obj.__dict__:
        if key == '__save_dict__':
            continue
        add_string = get_save_str(obj.__dict__[key])
        if add_string is not None:
            obj.__save_dict__.update({key: get_save_str(obj.__dict__[key])})

def load_protocols_dict(string_dict, prot_dict):
    """Specific function to load a protocol."""
    prot_dict.clear()
    for key in string_dict:
        prot_data = string_dict[key]
        prot = protocol_class.Measurement_Protocol()
        prot.name = key
        if 'loop_steps' in prot_data:
            prot.load_loop_steps(prot_data['loop_steps'])
        if 'plots' in prot_data:
            prot.plots = load_plots([], prot_data['plots'])
        if 'filename' in prot_data:
            prot.filename = prot_data['filename']
        if 'variables' in prot_data:
            prot.variables = prot_data['variables']
        if 'metadata' in prot_data:
            prot.metadata = prot_data['metadata']
        if 'channel_metadata' in prot_data:
            prot.channel_metadata = prot_data['channel_metadata']
        if 'config_metadata' in prot_data:
            prot.config_metadata = prot_data['config_metadata']
        if 'use_nexus' in prot_data:
            prot.use_nexus = prot_data['use_nexus']
        prot_dict.update({key: prot})

def load_devices_dict(string_dict, devices_dict):
    """Specific function to load devices."""
    devices_dict.clear()
    for key in string_dict:
        dev_data = string_dict[key]
        name = dev_data['name']
        try:
            dev_lib = importlib.import_module(f'{name}.{name}')
        except Exception as e:
            raise Exception(f'Could not import device module {name}\n{e}')
        dev = dev_lib.subclass()
        dev.name = name
        if 'connection' in dev_data:
            dev.connection = dev_data['connection']
        if 'virtual' in dev_data:
            dev.virtual = dev_data['virtual']
        if 'tags' in dev_data:
            dev.tags = dev_data['tags']
        if 'files' in dev_data:
            dev.files = dev_data['files']
        if 'directory' in dev_data:
            dev.directory = dev_data['directory']
        if 'requirements' in dev_data:
            dev.requirements = dev_data['requirements']
        if 'settings' in dev_data:
            dev.settings = dev_data['settings']
        if 'ioc_settings' in dev_data:
            dev.ioc_settings = dev_data['ioc_settings']
        if 'config' in dev_data:
            dev.config = dev_data['config']
        if 'custom_name' in dev_data:
            dev.custom_name = dev_data['custom_name']
        devices_dict.update({key: dev})



def get_most_recent_presets():
    """Goes through all files in the preset_path and returns the newest
    device-preset and measurement-preset.

    Returns
    -------
    pred : str
        name of the newest device-preset, returns None, if none found
    prem : str
        name of the neweset measurement-preset, returns None, if none found
    """
    presets = []
    for name in listdir(preset_path):
        if name.endswith('.preset'):
            presets.append(name)
    if presets:
        preset = sorted(presets, key=lambda x: os.path.getmtime(f'{preset_path}{x}'))[-1][:-7]
    else:
        preset = None
    return preset

def get_preferences():
    """If a file 'preferences.json' exists in the appdata, its content
    will be loaded and returned, if no file exists, it will be created
    with an empty dictionary."""
    if 'preferences.json' not in os.listdir(appdata_path):
        with open(f'{appdata_path}/preferences.json', 'w') as file:
            json.dump(standard_pref, file, indent=2)
    with open(f'{appdata_path}/preferences.json', 'r') as file:
        prefs = json.load(file)
    return prefs

def save_preferences(prefs:dict):
    """Saves the given dictionary prefs as 'preferences.json' in the appdata."""
    with open(f'{appdata_path}/preferences.json', 'w') as file:
        json.dump(prefs, file, indent=2)
