import json
import pickle
from abc import ABC, abstractmethod

from .components import Rule
from .errors import InvalidRuleError
from .parser import RuleParser


class RuleStorage(ABC):
    """
    Abstract base class for all storages that can store and load rules.
    """

    def __init__(self, *args, **kwargs) -> None:
        # parser to use for parsing the rule after it is laoded into a 'dict' format
        self.parser = RuleParser()

    @abstractmethod
    def load(self, *args, **kwargs) -> Rule:
        raise NotImplementedError('load method not implemented')

    @abstractmethod
    def store(self, rule: Rule, *args, **kwargs) -> None:
        raise NotImplementedError('store method not implemented')


class JSONRuleStorage(RuleStorage):
    """
    RuleStorage class for JSON files.
    """

    format = 'json'

    def __init__(self, file_path):
        """
        Initialize the loader with a file_path.
        """
        super().__init__()
        self.file_path = file_path
        # validate that the file_path is valid and is a json file
        if not self.file_path.endswith('.json'):
            raise InvalidRuleError('Invalid file type. Only JSON files are supported.')

    def load(self):
        """
        Load a rule from a JSON file.
        """
        data = {}
        with open(self.file_path) as f:
            data = json.load(f)
        return self.parser.parse(data)

    def store(self, rule):
        """
        Store a rule in a JSON file.
        """
        data = rule.to_dict()
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)


class JSONMultiRuleStorage(JSONRuleStorage):
  """
  Multiple RuleStorage class for JSON files.
  """


  def load(self):
      """
      Load a rule from a JSON file.
      """
      data = []
      with open(self.file_path) as f:
          data = json.load(f)
      if not isinstance(data, list):
        raise TypeError("Invalid data type")

      return [self.parser.parse(rule) for rule in data]

  def store(self, rules):
      """
      Store a list of rule in a JSON file.
      """
      if not isinstance(rules, list):
          raise TypeError("Invalid data type, expecting a list here")
      super().store(rules)


class PickledRuleStorage(RuleStorage):
    """
    RuleStorage class for Pickle files.
    """

    def __init__(self, file_path):
        """
        Initialize the loader with a file_path.
        """
        super().__init__()
        self.file_path = file_path

    def load(self):
        """
        Load a rule from a Pickle file.
        """
        data = {}
        with open(self.file_path, 'rb') as f:
            data = pickle.load(f)
        return self.parser.parse(data)

    def store(self, rule):
        """
        Store a rule in a Pickle file.
        """
        data = rule.to_dict()
        with open(self.file_path, 'wb') as f:
            pickle.dump(data, f)
