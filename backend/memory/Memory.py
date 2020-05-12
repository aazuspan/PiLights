import json
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
        Save a new value in memory. Can be used with an existing attribute or a new attribute.
        :param attribute : str name of memory attribute to save value for
        """
        memory_data = self.memory

        if attribute in memory_data:
            memory_data[attribute] = value

        with open(self.memory_file, 'w') as write_file:
            json.dump(memory_data, write_file)
    
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
