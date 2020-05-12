import json
import logging
import os

class Memory:
    memory_file = os.path.join(os.getcwd(), 'memory', 'memory.json')

    @property
    def memory(self):
        """
        Read and return the contents of the current memory file
        :return : dict of memory data
        """
        with open(self.memory_file, 'r') as f:
            memory_data = json.load(f)
        
        return memory_data

    def load(self, attribute):
        """
        Load the value of an attribute stored in memory
        :param attribute : str name of memory attribute to load value for
        :return : str/int/float value stored in memory for the requested attribute
        """
        value = None

        memory_data = self.memory
        
        if attribute in memory_data:
            value = memory_data[attribute]

        return value

    def save(self, attribute, value):
        """
        Save a new value in memory. Can only be used with an existing attribute
        :param attribute : str name of memory attribute to save value for
        :param value: str value to save for that attribute
        """
        memory_data = self.memory

        if attribute in memory_data:
            memory_data[attribute] = value

        else:
            logging.warn('Attempted to save {} value into memory, but {} does not exist in memory!'.format(attribute, attribute))

        with open(self.memory_file, 'w') as write_file:
            json.dump(memory_data, write_file)
    
    def save_setting(self, setting, value):
        """
        Save a new setting value in memory. Can be used with an existing setting.
        :param setting : str name of memory attribute to save value for
        :param value: str value to save for that attribute
        """
        memory_data = self.memory

        if setting in memory_data['settings']:
            memory_data['settings'][setting]['current_value'] = value
        else:
            logging.warn('Attempted to save {} value into memory, but {} does not exist in memory!'.format(setting, setting))

        with open(self.memory_file, 'w') as write_file:
            json.dump(memory_data, write_file)

    
    def save_settings(self, settings):
        """
        Save a batch of settings into memory
        :param settings: Dictionary of {setting name: value} pairs
        """
        for key in settings.keys():
            self.save_setting(key, settings[key])

    def get_settings(self):
        """
        Return all settings stored in memory
        :return : List of dictionaries representing the parameters of each setting
        """
        memory_data = self.memory
        settings = []

        setting_keys = memory_data['settings'].keys()

        for key in setting_keys:
            settings.append(memory_data['settings'][key])
        
        return settings
