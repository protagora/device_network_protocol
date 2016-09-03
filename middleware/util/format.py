import json


class UtilityConfigurationException(Exception):
    pass


class ConfigurationFormat(object):

    def encode(self):
        pass

    def decode(self):
        pass


class ConfigurationFormatJson(ConfigurationFormat):

    ERROR_ENCODING_JSON = "Error encoding object to JSON string"
    ERROR_DECODING_JSON = "Error decoding JSON string to object"
    ERROR_STRING_EXPECTED = "Expected string, {} given"
    ERROR_PRIMITIVE_EXPECTED = "Expected list, dict, tuple or set, {} given"

    def encode(self, obj=None):
        try:
            assert isinstance(obj, (list, dict, tuple, set))
        except:
            raise UtilityConfigurationException(self.ERROR_PRIMITIVE_EXPECTED.format(type(obj)))
        try:
            return json.dumps(obj)
        except:
            raise UtilityConfigurationException(self.ERROR_ENCODING_JSON)

    def decode(self, string=None):
        try:
            assert isinstance(string, str)
        except:
            raise UtilityConfigurationException(self.ERROR_STRING_EXPECTED.format(type(string)))
        try:
            return json.loads(string)
        except:
            raise UtilityConfigurationException(self.ERROR_DECODING_JSON)


class ConfigurationFormatFactory(object):

    FORMAT_JSON = 'json'

    FORMAT = {
        FORMAT_JSON: ConfigurationFormatJson
    }

    ERROR_FORMAT_NOT_SUPPORTED = "Configuration format not supported: {}"

    def create(self, config_format=None):
        try:
            assert config_format in self.FORMAT
            instance = self.FORMAT[config_format]()
            assert issubclass(instance.__class__, ConfigurationFormat)
            return instance
        except:
            try:
                config_format = repr(config_format)
            except (BaseException, ):
                config_format = type(config_format)
            raise UtilityConfigurationException(self.ERROR_FORMAT_NOT_SUPPORTED.format(config_format))
