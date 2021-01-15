from ...utils import rest
from ...utils.api import from_api_json
from ...utils.checks import check_datetime, check_date
from ...utils.resource import Resource
from ..__transfer import _resource as _transfer_resource


class Log(Resource):
    """# transfer.Log object
    Every time a Transfer entity is modified, a corresponding transfer.Log
    is generated for the entity. This log is never generated by the
    user.
    ## Attributes:
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - transfer [Transfer]: Transfer entity to which the log refers to.
    - errors [list of strings]: list of errors linked to this BoletoPayment event.
    - type [string]: type of the Transfer event which triggered the log creation. ex: "processing" or "success"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, created, type, errors, transfer):
        Resource.__init__(self, id=id)

        self.created = check_datetime(created)
        self.type = type
        self.errors = errors
        self.transfer = from_api_json(_transfer_resource, transfer)


_resource = {"class": Log, "name": "TransferLog"}


def get(id, user=None):
    """# Retrieve a specific transfer.Log
    Receive a single transfer.Log object previously created by the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - transfer.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, types=None, transfer_ids=None, user=None):
    """# Retrieve transfer.Log's
    Receive a generator of transfer.Log objects previously created in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by types. ex: "success" or "failed"
    - transfer_ids [list of strings, default None]: list of Transfer ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Project object, default None]: Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of transfer.Log objects with updated attributes
    """
    return rest.get_list(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        transfer_ids=transfer_ids,
        user=user,
    )
