# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import configs
import requests
import bonobo
import csv
import copy

from json.decoder import JSONDecodeError
from bonobo.config import Option, use_context
from bonobo.constants import NOT_MODIFIED
from bonobo.util import ensure_tuple

from logging_ import logging

logger = logging.getLogger(__name__)

def transform_keys(jsonobj, root, parentkey):
    logger.info(f'Transforming with parentkey={parentkey} ')
    if type(jsonobj) is not dict:
        root[parentkey] = jsonobj
        logger.debug(f'Return sub-dict {root}.')
        return root

    for key, value in jsonobj.items():
        _parentkey = key if parentkey is None else f'{parentkey}_{key}'
        logger.debug(f'Formating sub-dict value={value} | root={root} | parentkey={parentkey}.')
        transform_keys(value, root=root, parentkey=_parentkey)
    return root

def get_list_field(field_name, attach_fields=None):
    def _get_list_field(row):
        logger.info(f'Extracting list field "{field_name}"')
        result = {field_name: row.get(field_name, [])}
        if attach_fields is not None:
            logger.debug(f'Attaching fields "{attach_fields}" to the result...')
            result.update({key: row.get(key) for key in attach_fields})
        return result
    return _get_list_field

def pop_fields(*fields) :
    def _pop_field(row):
        logger.debug(f'Removing fields {fields} from the result')
        for field in fields:
            if field in row:
                logger.debug(f'Popping "{field}" from the result')
                row.pop(field)
        return row
    return _pop_field




