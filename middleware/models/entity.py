import json
import os


class ConfigurationStructure(object):

    def __init__(self, data=None):
        try:
            assert isinstance(data, dict)
            self.data = data
        except (BaseException, ):
            pass

    def get(self, key=None, path=None):
        pass


class Hydrator(object):

    FIELDS = []

    def __init__(self, data=None):
        for field in self.FIELDS:
            setattr(self, field, None)
        try:
            self.hydrate(data=data)
        except (BaseException, ):
            raise

    def hydrate(self):
        pass

    def extract(self):
        pass


class Configurable(Hydrator):

    def hydrate(self, data):
        try:
            assert isinstance(data, dict)
        except (BaseException, ):
            return
        for field, value in data.items():
            try:
                assert field in self.FIELDS
                setattr(self, field, value)
            except (BaseException, ):
                pass

    def extract(self):
        return {field: getattr(self, field, None) for field in self.FIELDS}

    def __getattr__(self, item):
        try:
            assert item in self.FIELDS
        except (BaseException, ):
            raise AttributeError("Attribute not found")
        return super().__getattr__(item)

    def __setattr__(self, key, value):
        try:
            assert key in self.FIELDS
        except (BaseException, ):
            raise AttributeError("Attribute not found")
        try:
            validator = getattr(self, "validate_{}".format(key))
        except (BaseException, ):
            validator = None
        if hasattr(self, key) and validator and callable(validator):
            validator(value)
        return super(Configurable, self).__setattr__(key, value)

    def __str__(self):
        return str(getattr(self, self.FIELDS[0]))

    def _is_integer(self, integer, _min=None, _max=None, inclusive=False):
        try:
            assert isinstance(integer, int)
        except (BaseException, ):
            raise ValueError("Integer expected")
        if _min is not None:
            try:
                assert isinstance(_min, int)
                assert _min >= 0
                if inclusive is not False:
                    assert integer >= _min
                else:
                    assert integer > _min
            except (BaseException, ):
                raise ValueError("Integer smaller then a minimum")
        if _max is not None:
            try:
                assert isinstance(_max, int)
                assert _max > 0
                if inclusive is not False:
                    assert integer <= _max
                else:
                    assert integer < _max
            except (BaseException, ):
                raise ValueError("Integer larger then a maximum")
        return self

    def _is_string(self, string, min_length=None, max_length=None, inclusive=False):
        try:
            assert isinstance(string, str)
        except (BaseException, ):
            raise ValueError("String expected")
        if min_length is not None:
            try:
                assert isinstance(min_length, int)
                assert min_length >= 0
                try:
                    if inclusive is not False:
                        assert len(string) >= min_length
                    else:
                        assert len(string) > min_length
                except (BaseException, ):
                    raise ValueError("String shorter then minimum length")
            except (BaseException, ):
                pass
        if max_length is not None:
            try:
                assert isinstance(max_length, int)
                assert max_length > 0
                try:
                    if inclusive is not False:
                        assert len(string) <= max_length
                    else:
                        assert len(string) < max_length
                except (BaseException, ):
                    raise ValueError("String larger then maximum length")
            except (BaseException, ):
                pass
        return self

    def _is_list(self, target, non_empty=True, min_length=None, max_length=None, inclusive=False):
        try:
            assert isinstance(target, list)
        except (BaseException, ):
            raise ValueError("List expected, {} encountered".format(type(target)))
        if non_empty is not True:
            try:
                assert len(target) > 0
            except (BaseException, ):
                raise ValueError("Non-empty list expected")
        if min_length is not None:
            try:
                assert isinstance(min_length, int)
                assert min_length >= 0
                try:
                    if inclusive is not False:
                        assert len(target) >= min_length
                    else:
                        assert len(target) > min_length
                except (BaseException, ):
                    raise ValueError("String shorter then minimum length")
            except (BaseException, ):
                pass
        if max_length is not None:
            try:
                assert isinstance(max_length, int)
                assert max_length > 0
                try:
                    if inclusive is not False:
                        assert len(target) <= max_length
                    else:
                        assert len(target) < max_length
                except (BaseException, ):
                    raise ValueError("String larger then maximum length")
            except (BaseException, ):
                pass
        return self

    def _is_dictionary(self, target, non_empty=True):
        try:
            assert isinstance(target, dict)
        except (BaseException, ):
            raise ValueError("Dictionary expected, {} encountered".format(type(target)))
        if non_empty is not True:
            try:
                assert len(target) > 0
            except (BaseException, ):
                raise ValueError("Non-empty dictionary expected")
        return self


class EntityConfiguration(Hydrator):

    """ Configuration structure JSON
        {
            'entity': { //entity can be one of following, components, resources
                'id': { //id is unique id of the entity (component_id or resource_id)
                    'name': {
                        'flags': int,
                        'description': str,
                        ['value': type,]
                        ['fields': []] //presence of 'flags' qualifies it as a structure
                    }
                }
            }
        }

        Example usage

        configuration = Configuration(config_file='path/to/config/file.json')
        configuration.set(key='init_function', value='parsable_init_function_representation')
        configuration.save()

        entire_configuration = configuration.get()
    """

    FIELDS = ['configuration', 'configuration_file']

    KEYS = ['flags', 'name', 'description', 'value', 'fields']

    def __init__(self, data=None, config_file=None):
        for field in self.FIELDS:
            setattr(self, field, None)
        try:
            assert config_file is not None
        except (BaseException, ):
            raise Exception("Configuration file must be provided")
        try:
            assert os.path.exists(config_file)
        except (AssertionError, ):
            try:
                with open(config_file, 'w') as handle:
                    handle.close()
            except (BaseException, ):
                raise Exception("Error creating config file: {}".format(config_file))
        self.configuration_file = config_file
        self.configuration = self.get()
        if data is not None:
            self.configuration = data

    def hydrate(self, data):
        try:
            assert data is None or not data
            return
        except (BaseException, ):
            pass
        try:
            assert isinstance(data, str)
            data = json.loads(data)
        except AssertionError:
            pass
        except json.decoder.JSONDecodeError:
            raise ValueError("Component configuration expect JSON parsable string")
        except (BaseException, ):
            raise ValueError("Error decoding JSON string")
        try:
            assert isinstance(data, dict)
        except (BaseException, ):
            raise Exception("Component configuration hydrate method expects a dictionary")
        self.configuration = data

    def extract(self):
        return self.configuration

    def save(self):
        try:
            with open(self.configuration_file, 'w') as handle:
                handle.write(json.dumps(self.configuration))
        except (BaseException, ):
            raise Exception("Error saving configuration")

    def get(self, key=None):
        if self.configuration is not None:
            configuration = self.configuration.copy()
        else:
            try:
                with open(self.configuration_file, 'r') as handle:
                    data = handle.read()
                    if len(data) == 0:
                        data = "{}"
                    configuration = json.loads(data)
                assert isinstance(configuration, dict)
            except (BaseException, ):
                raise Exception("Error reading configuration file {}".format(self.configuration_file))
        if key is not None:
            try:
                assert isinstance(key, str) and len(key) > 0
            except (BaseException, ):
                raise Exception("Only string keys are permitted")
            try:
                assert key in configuration.keys()
                configuration = configuration[key]
            except (BaseException, ):
                raise Exception("Key not found")
        return configuration

    def set(self, key=None, value=None):
        try:
            assert self.configuration is not None
            assert isinstance(self.configuration, dict)
        except (BaseException, ):
            raise Exception("Configuration not available")
        try:
            self.configuration[key] = value
        except (BaseException, ):
            raise Exception("Something went wrong")


class ResourceConfiguration(Hydrator):

    def hydrate(self, data):
        pass

    def extract(self):
        pass


class ComponentRow(Configurable):

    FIELDS = ["id", "status", "name", "description", "resource_table", "init_function", "config"]

    def validate_id(self, _id):
        self._is_integer(_id, 1, 2 ** 16 - 1, True)

    def validate_status(self, status):
        self._is_integer(status, 0, 2**8 - 1)

    def validate_description(self, description):
        self._is_string(description, max_length=2**8 - 1)

    def validate_resource_table(self, resource_table):
        self._is_string(resource_table, max_length=2**8 - 1)

    def validate_init_function(self, init_function):
        self._is_string(init_function, max_length=2**8 - 1)

    def validate_config(self, config):
        self._is_string(config, max_length=2**8 - 1)


class ResourceRow(Configurable):

    FIELDS = ['id', 'status', 'name', 'description', 'read_function', 'write_function', 'init_function', 'config']

    def validate_id(self, _id):
        self._is_integer(_id, 1, 2**16 - 1, True)

    def validate_status(self, status):
        self._is_integer(status, 0, 2**8 - 1, True)

    def validate_description(self, description):
        self._is_string(description, 2**8 - 1)

    def validate_read_function(self, read_function):
        self._is_string(read_function, max_length=2**8 - 1)

    def validate_write_function(self, write_function):
        self._is_string(write_function, max_length=2**8 - 1)

    def validate_init_function(self, init_function):
        self._is_string(init_function, max_length=2**8 - 1)

    def validate_config(self, config):
        self._is_string(config, max_length=2**8 - 1)


class ServiceConfiguration(Configurable):

    FIELDS = ["components", "resources"]
    EMPTY_RESPONSE = {"components": dict(), "resources": dict()}

    def hydrate(self, data):
        try:
            assert isinstance(data, dict)
        except (BaseException, ):
            return
        if 'components' in data.keys():
            for item in data['components']:
                self._hydrate(item, 'components')
        if 'resources' in data.keys():
            for item in data['resources']:
                self._hydrate(item, 'resources')

    def extract(self):
        response = {"components": dict(), "resources": dict()}
        for _id, item in self.components.items():
            response["components"][str(item)] = item.extract()
        for _id, item in self.resources.items():
            response["resources"][str(item)] = item.extract()
        return response

    def __str__(self):
        response = {'components': list(), 'resources': list()}
        try:
            for item in self.components:
                response['components'].append(str(item))
        except (BaseException, ):
            pass
        try:
            for item in self.resources:
                response['resources'].append(str(item))
        except (BaseException, ):
            pass
        return "components: {}, resources: {}.".format(', '.join(response['components']), ', '.join(response['resources']))

    def _hydrate(self, item=None, type=None):
        if item is None:
            return
        if isinstance(item, dict):
            if 'components' == type:
                try:
                    item = ComponentRow(item)
                except (BaseException, ):
                    pass
            if 'resources' == type:
                try:
                    item = ResourceRow(item)
                except (BaseException, ):
                    pass
        if isinstance(item, ComponentRow):
            if self.components is None:
                self.components = dict()
            self.components[str(item)] = item
        if isinstance(item, ResourceRow):
            if self.resources is None:
                self.resources = dict()
            self.resources[str(item)] = item


class QualityOfService(object):

    METRIC = {
        'response_time': ResponseTimeMetric,
        'throughput': ThroughputMetric
    }

    def __init__(self):
        pass

    # communication is a dictionary of sequential request and responses
    # preformed by middleware
    # communication = {
    #                   1: {'request': request, 'response': response'},
    #                   2: {'request': request, 'response': response}
    # }
    # metric = type of metric to performe, self.METRIC value
    def save(self, communication, metrics):
        pass

    def read(self, idp=None, metrics=None):
        pass


class Metric(object):

    def __init__(self, communication=None):
        self.communication = communication


class ResponseTimeMetric(Metric):

    def __init__(self, communication=None):
        super().__init__(communication=communication)


class ThroughputMetric(Metric):

    def __init__(self, communication=None):
        super().__init__(communication=communication)


if "__main__" == __name__:

    component_data = {'id': 1, 'status': 5, 'resource_table': '1', 'name': 'Test name',
                      'description': 'Description of the component', 'config': 'configuration_handler',
                      'init_function': 'init_handler'}
    component = ComponentRow(component_data)
    print(component.extract())

    resource_data = {'id': 7, 'status': 255, 'description': 'Resource description', 'write_function': 'write',
                     'read_function': 'read', 'init_function': 'init', 'config': 'configuration', 'name': 'resource'}

    resource = ResourceRow(resource_data)
    print(resource.extract())

    service = ServiceConfiguration({"components": [component], "resources": [resource]})
    print(service.extract())

    from dna.settings import BASE_PATH
    configuration = EntityConfiguration(config_file="{}/config/device.json".format(BASE_PATH))
    configuration.set(key="init_function", value="init")
    configuration.save()

    print(configuration.get())
