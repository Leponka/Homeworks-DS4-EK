from enum import Enum

token = '1340309822:AAHCW_OO_fL0yADM9KtzTc2DOPDADAdmWrM'

db_file = 'database.vdb'

class states(Enum):
    S_START = '0'
    S_LIST_OR_COUNTRY = '1'
    S_TAIL_LIST = '3'
    S_HEAD_LIST = '4'
    S_COUNTRY = '5'


