import imp
import inspect
import os
import sys
from os.path import abspath
import yaml
from imp import load_module


class PluginLoadException(Exception):
    pass


class BasePlugin(object):
    def run(self):
        raise NotImplementedError


class Plugin(object):
    _plugins = {}

    @classmethod
    def load_plugins(cls, plugin_dir):
        """ Load external plugins."""
        for i in os.listdir(plugin_dir):
            cls.load_plugin(os.path.join(abspath(plugin_dir), i))

    @classmethod
    def load_plugin(cls, path):
        cls.validate_plugin(path)
        with open(os.path.join(path, 'plugin.yaml'), 'r') as f:
            try:
                plugin = yaml.safe_load(f)
                entry = plugin.get('runtime').get('main')
                module, clz = entry.split(':')
                f, path, desc = imp.find_module(module, [path])
                module = imp.load_module(f'{module}.{clz}', f, path, desc)
                getattr(module, clz)().run()

            except yaml.YAMLError as exc:
                print(exc)

    @classmethod
    def validate_plugin(cls, path):
        cls.validate_is_dir(path)
        cls.validate_dir_contains_plugin_yaml(path)

    @staticmethod
    def validate_is_dir(path):
        if not os.path.isdir(path):
            raise PluginLoadException('plugin should be a dir')

    @staticmethod
    def validate_dir_contains_plugin_yaml(path):
        if not os.path.exists(os.path.join(path, 'plugin.yaml')):
            raise PluginLoadException('plugin dir should contain plugins yaml')
