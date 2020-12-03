import requests
import bonobo
import configs 

from json.decoder import JSONDecodeError

from lib import transform_keys, get_list_field, pop_fields, logger
from logging_ import logging


logger = logging.getLogger(__name__)


def extract(
    vid_offset=None, 
    time_offset=None, 
    count_per_page=configs.RECENT_UPDATED_CONTACT_COUNT_PER_PAGE, 
    api_key=configs.HUBSPOT_API_KEY):
    """
    Generator to get contacts from Hubspot API.
    
    param: vid_offset string (default None) (&vidOffset=X - Used in the request URL) Another method used to page through
    the recent contacts. Every call to this endpoint will return a vid-offset value. This value is used in the vidOffset
    parameter of the next call to get the next page of contacts.
    
    param: time_offset: string (default None) (&timeOffset=X - Used in the request URL)	One method used to page through
    the recent contacts. Every call to this endpoint will return a time-offset value. This value is used in the timeOffset
    parameter of the next call to get the next page of contacts. The preferred method of paging.

    param: count_per_page: int (defaults to the configuration constant RECENT_UPDATED_CONTACT_COUNT_PER_PAGE) (&count=X -
    Used in the request URL) This parameter lets you specify the amount of contacts to return in your API call. The default
    for this parameter (if it isn't specified) is 20 contacts. The maximum amount of contacts you can have returned to you 
    via this parameter is 100.
    
    param: api_key: string (defaults to the configuration constant HUBSPOT_API_KEY) (&hapikey=X - Used in the request URL)
    The api key to authenticate through the API.

    yield: dict contact object for each iteration.
    """

    params = {
        'hapikey': api_key,
        'count': count_per_page,
        'vidOffset': vid_offset,
        'timeOffset': time_offset
    }

    logger.info(f'Getting data from remote server url: {configs.HUBSPOT_RECENTLY_UPDATED_CONTACTS_URL} && params={params}')
    response = requests.get(configs.HUBSPOT_RECENTLY_UPDATED_CONTACTS_URL, params=params)
    if response.status_code != 200:
        logger.warning(f'The request was not successful, responded with status code {response.status_code}.')
        logger.debug(f'Error response data = {response.text}')
        return None
    try:
        result = response.json()
        logger.info(f'Request was successful....')
        logger.debug(f'Response data = f{result}')
    except (ValueError, JSONDecodeError) as e:
        logger.exception(e)
        return None 
        
    contacts = result.get('contacts', [])
    has_more = result.get('has-more', False)
    
    yield from contacts

    # If there is still more contacts, then get them using recursion.
    if has_more:
        logger.info('Fetching more data ....')
        vid_offset = result.get('vid-offset')
        time_offset = result.get('time_offset')
        yield from extract(vid_offset=vid_offset, time_offset=time_offset)

    logger.info('Extracted all data, see you next time :) ')


def transform(row):
    logger.debug(f'Transforming: {row}')
    transformed_row = transform_keys(row, {}, None)
    logger.debug(f'Result after transformation: {row}')
    return transformed_row

def get_graph(**options):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph

    """
    logger.info(f'Building the graph..')
    logger.debug(f'Building the graph with options={options}.')
    graph = bonobo.Graph(
        extract,
    )

    # Add transform nodes
    transform_properties = graph.add_chain(
        get_list_field('properties', attach_fields=('vid',)), 
        transform, 
        _input=extract, 
        _name='transform_properties')

    transform_form_submissions = graph.add_chain(
        get_list_field('form-submissions', attach_fields=('vid',)),
        # The following line is important because the output is list of lists.
        # lambda row: row[0],
        transform,
        _input=extract,
        _name='transform_form-submissions')

    transform_other_fields = graph.add_chain(
        pop_fields('properties', 'form-submissions'),
        transform,
        _input=extract,
        _name='transform_other_fields')

    # Add load nodes
    graph.add_chain(
        bonobo.UnpackItems(0),
        bonobo.CsvWriter(configs.OUTPUT_PROPERTIES_FILE),
        _input=transform_properties.output,
        _name="load_properties"
    )

    graph.add_chain(
        bonobo.UnpackItems(0),
        bonobo.CsvWriter(configs.OUTPUT_FORM_SUBMISSIONS_FILE),
        _input=transform_form_submissions.output,
        _name="load_form-submissions"
    )

    graph.add_chain(
        bonobo.UnpackItems(0),
        bonobo.CsvWriter(configs.OUTPUT_OTHER_FIELDS_FILE),
        _input=transform_other_fields.output,
        _name="load_all_other_fields"
    )

    return graph

def get_services(**options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {}


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        graph = get_graph(**options)
        logger.debug(f'Graph Inspection: {graph._repr_dot_()}')
        bonobo.run(
            graph,
            services=get_services(**options)
        )