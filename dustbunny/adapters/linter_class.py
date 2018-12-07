from abc import ABC, ABCMeta, abstractmethod
from typing import NamedTuple, Tuple
from collections import namedtuple
from pandas import DataFrame


TemplateType = Tuple[Tuple[str, type]]


class Linter(ABC):
    '''
    Linter abstract base class.
    
    '''
    Item = None
    Result = None
    
    @classmethod
    @abstractmethod
    def result_template(cls) -> TemplateType:
        return (
            ('placeholder', str),
        )
    
    @classmethod
    @abstractmethod
    def item_template(cls) -> TemplateType:
        return (
            ('placeholder', str),
        )

    @classmethod
    def load_namedtuple(cls, internal_name: str, template: TemplateType):
        return NamedTuple(f'{cls.__name__}{internal_name}', template)

    @classmethod
    def load_internal_classes(cls):
        cls.Item = cls.load_namedtuple('Item', cls.item_template())
        cls.Result = cls.load_namedtuple('Result', cls.result_template())

    def __init__(self) -> type(None):
        self.__class__.load_internal_classes()
        self.target_path = None
        self.result = None
        self.update()

    @abstractmethod
    def update(self):
        ...

    def retarget(self, new_target: str):
        self.target_path = new_target
        self.update()
        
    # @abstractmethod
    def report(self) -> str:
        '''
		Generates a report text block intended for consumption by dustbunny user.
		Should be clearly formatted and human-readable.
		'''
        if self.result is None:
            self.update()
            if self.result is None:
                return ''
        report_text = '\n'
        for field in self.result:
            report_text += (str(field) + '\n')
        return report_text

    @property
    @abstractmethod
    def data(self) -> DataFrame:
        if isinstance(self.result.data, DataFrame):
            return self.result.data
        else:
            return DataFrame()
    

class AbstractBaseLinter(object):
    ''''''
    __metaclass__ = ABCMeta
    _ResultClass = None

    @classmethod
    def build_result_class(cls):
        template = cls.result_template()
        ResultClass = NamedTuple(f'{cls.__name__.capitalize()}Result', template)
        return ResultClass

    # def __init__(self):
    #     my_class = type(self)
    #     ResultClass = type(self).build_result_class()

    @property
    @abstractmethod
    def result_template(cls):
        template = (
            ('placeholder', str)
        )
        return template

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def retarget(self, new_target: str):
        self.target_path = new_target
        self.update()

    @abstractmethod
    def report(self) -> str:
        '''
        Generates a report text block intended for consumption by dustbunny user.
        Should be clearly formatted and human-readable.
        '''
        if self.result is None:
            self.update()
        report_text = '\n'
        for field in self.result:
            report_text += (str(field) + '\n')
        return report_text
    
    @property
    @abstractmethod
    def data(self) -> DataFrame:
        ...



