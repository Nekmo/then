from dataclasses import dataclass

from then.configs.base import LoadConfigBase


@dataclass
class LoadComponentConfigs(LoadConfigBase):
    path: str
    sections: str = 'components'
