import os
from dna.middleware.util.format import ConfigurationFormatFactory


class ConfigurationException(Exception):
    pass


class Configuration(object):

    # file write formats: json, yaml, xml...
    FORMAT_JSON = ConfigurationFormatFactory.FORMAT_JSON

    ERROR_READING_CONFIG = "Error reading configuration"
    ERROR_WRITING_CONFIG = "Error writing configuration"
    ERROR_NOT_EXISTS = "Configuration path doesn't exist"
    ERROR_NOT_FILE = "Configuration path is not a file"
    ERROR_NOT_WRITABLE = "Configuration path not writable"
    ERROR_SAVING = "Error saving configuration"
    ERROR_KEY = "Path not traversable, key not found: {}"
    ERROR_NOT_FOUND = "Not found"
    ERROR_SETTING_KEY = "Setting key '{}' to value '{}' failed"
    ERROR_INITIALIZING_CONFIG = "Error initializing configuration file"

    def read(self):
        pass

    def write(self, configuration=None):
        pass


class JsonConfiguration(Configuration):

    DEFAULT_FORMAT = ConfigurationFormatFactory.FORMAT_JSON
    DEFAULT_CONFIG = "{}"

    def __init__(self, path, config_format=None):
        self.path = path
        if config_format:
            self.format = config_format
        else:
            self.format = self.DEFAULT_FORMAT
        self.configuration_factory = ConfigurationFormatFactory()
        self.codec = self.configuration_factory.create(config_format=self.format)
        self.__configuration = None
        self._test()

    @property
    def configuration(self):
        if self.__configuration is None:
            self.read()
        return self.__configuration

    @configuration.setter
    def configuration(self, configuration=None):
        self.__configuration = configuration

    def save(self):
        try:
            self.write()
        except:
            raise ConfigurationException(self.ERROR_SAVING)

    def _test(self):
        try:
            assert os.path.exists(self.path)
        except:
            raise ConfigurationException(self.ERROR_NOT_EXISTS)
        try:
            assert os.path.isfile(self.path)
        except:
            raise ConfigurationException(self.ERROR_NOT_FILE)
        try:
            with open(self.path, 'r') as handle:
                data = handle.read()
            if not data:
                with open(self.path, 'w') as handle:
                    handle.write(self.DEFAULT_CONFIG)
        except:
            raise ConfigurationException(self.ERROR_INITIALIZING_CONFIG)

    def get(self, key=None, path=None):
        data = self.configuration
        if path is not None:
            for item in path:
                try:
                    data = data[item]
                except:
                    raise ConfigurationException(self.ERROR_KEY.format(item))
        try:
            return data[key]
        except:
            raise ConfigurationException(self.ERROR_NOT_FOUND)

    def set(self, key=None, value=None, path=None):
        data = self.configuration
        if path is not None:
            for item in path:
                try:
                    if isinstance(data, dict):
                        if item not in data.keys():
                            data[item] = dict()
                    elif isinstance(data, list):
                        if isinstance(item, int) and item >= 0:
                            if item > len(data) - 1:
                                for index in range(len(data), item + 1):
                                    data.append(dict())
                    data = data[item]
                except:
                    raise ConfigurationException(self.ERROR_KEY.format(item))
        try:
            data[key] = value
        except:
            raise ConfigurationException(self.ERROR_SETTING_KEY.format(key, value))

    def read(self):
        try:
            with open(self.path, 'r') as handle:
                self.configuration = self.codec.decode(handle.read())
        except:
            raise ConfigurationException(self.ERROR_READING_CONFIG)
        return self.configuration

    def write(self, configuration=None):
        try:
            assert configuration is not None
            self.configuration = configuration
        except (BaseException, ):
            pass
        try:
            with open(self.path, 'w') as handle:
                handle.write(self.codec.encode(obj=self.configuration))
        except (BaseException, ):
            raise ConfigurationException(self.ERROR_WRITING_CONFIG)


class EntityConfiguration(object):

    def __init__(self, configuration_file=None):
        try:
            assert os.path.exists(configuration_file)
            assert os.path.isfile(configuration_file)
        except (BaseException, ):
            raise ConfigurationException("Configuration file not found")
        self.configuration_file = configuration_file
        try:
            with open(self.configuration_file, 'r') as handle:
                self.configuration = handle.read()
        except (BaseException, ):
            raise ConfigurationException("Error reading configuration file: {}".format(self.configuration_file))

    def get(self, key=None, path=None):
        _configuration = self.configuration
        for step in path:
            try:
                _configuration = _configuration[step]
            except (BaseException, ):
                return None
        try:
            return _configuration[key]
        except (BaseException, ):
            return None

    def set(self, key=None, value=None, path=None):
        _configuration = self.configuration
        for step in path:
            if isinstance(_configuration, dict):
                try:
                    step = str(step)
                except (BaseException, ):
                    ConfigurationException("Path may only contain strings and integers, {} encountered".format(type(step)))
                if step not in _configuration.keys():
                    _configuration[step] = dict()
            else:
                if isinstance(_configuration, list):
                    try:
                        step = int(step)
                    except (BaseException, ):
                        ConfigurationException("Path may only contain strings and integers, {} encountered".format(type(step)))
                    if step > len(_configuration):
                        while len(_configuration) - 1 < step:
                            _configuration.append(dict())
                        _configuration[step] = dict()
                else:
                    return False
        _configuration[key] = value
        return True

    def save(self):
        try:
            with open(self.configuration_file, 'w') as handle:
                handle.write(self.configuration)
        except (BaseException, ):
            ConfigurationException("Error saving configuration file")


class ServiceConfiguration(EntityConfiguration):

    COMPONENT = ['id', 'status', 'name', 'description', 'resource_table', 'init_function', 'config']
    RESOURCE = ['id', 'status', 'name', 'description', 'read_function', 'write_function', 'init_function', 'config']

    def get_component(self, _id=None):
        pass

    def add_component(self, data=None):
        pass

    def get_resource(self, _id=None):
        pass

    def add_resource(self, data=None):
        pass

    def get(self, entity=None, _id=None):
        pass

    def set(self, entity=None, _id=None):
        pass

    def save(self):
        pass


class ComponentConfiguration(EntityConfiguration):

    pass


class ResourceConfiguration(EntityConfiguration):

    pass


# # # TEST # # #
if "__main__" == __name__:
    # from dna.settings import *
    # _path = "{}{}".format(BASE_PATH, '/config/device.json')
    # print(_path)
    # simple_config = JsonConfiguration(path=_path)
    # __configuration = simple_config.read()
    #
    # # explicit by write
    # __configuration["version"] = "1.1.7"
    # simple_config.write(configuration=__configuration)
    #
    # print(__configuration)
    #
    # # implicit by save
    # try:
    #     print("configuration value (pre): " + simple_config.get(key="key", path=["path", "test", 0]))
    # except (BaseException, ):
    #     pass
    # simple_config.set(key="key", value="new value", path=["path", "test", 0])
    # print("configuration value (post): " + simple_config.get(key="key", path=["path", "test", 0]))
    # simple_config.set(key="key1", value="new value 1", path=["path 3", "test 4", 7])
    # simple_config.set(key="key", value="new value 1", path=["path", "test", 7])
    # print("new: " + simple_config.get(key="key1", path=["path 3", "test 4", 7]))
    # simple_config.save()
    pass
