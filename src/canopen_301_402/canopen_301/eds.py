#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict
from ConfigParser import RawConfigParser
from flufl.enum import Enum

class EdsFileInfo(object):
    """docstring for EdsFileInfo"""
    def __init__(self, dictionary):
        super(EdsFileInfo, self).__init__()
        self.created_by = dictionary["CreatedBy"]
        self.modified_by = dictionary["ModifiedBy"]
        self.description = dictionary["Description"]
        self.creation_time = dictionary["CreationTime"]
        self.creation_date = dictionary["CreationDate"]
        self.modification_time = dictionary["ModificationTime"]
        self.modification_date = dictionary["ModificationDate"]
        self.file_name = dictionary["FileName"]
        self.file_version = dictionary["FileVersion"]
        self.file_revision = dictionary["FileRevision"]
        self.eds_version = dictionary["EDSVersion"]
        
class EdsDeviceInfo(object):
    """docstring for EdsDeviceInfo"""
    def __init__(self, dictionary):
        super(EdsDeviceInfo, self).__init__()
        self.vendor_name = dictionary["VendorName"]
        self.vendor_number = dictionary["VendorNumber"]
        self.product_name = dictionary["ProductName"]
        self.product_number = dictionary["ProductNumber"]
        self.revision_number = dictionary["RevisionNumber"]
        self.order_code = dictionary["OrderCode"]
        self.baudrate_10 = dictionary["BaudRate_10"]
        self.baudrate_20 = dictionary["BaudRate_20"]
        self.baudrate_50 = dictionary["BaudRate_50"]
        self.baudrate_125 = dictionary["BaudRate_125"]
        self.baudrate_250 = dictionary["BaudRate_250"]
        self.baudrate_500 = dictionary["BaudRate_500"]
        self.baudrate_800 = dictionary["BaudRate_800"]
        self.baudrate_1000 = dictionary["BaudRate_1000"]
        self.simple_boot_up_master = dictionary["SimpleBootUpMaster"]
        self.simple_boot_up_slave = dictionary["SimpleBootUpSlave"]
        self.granularity = dictionary["Granularity"]
        self.dynamic_channels_supported = dictionary["DynamicChannelsSupported"]
        self.compact_pdo = dictionary["CompactPDO"]
        self.group_messaging = dictionary["GroupMessaging"]
        self.nr_of_rxpdo = dictionary["NrOfRXPDO"]
        self.nr_of_txpdo = dictionary["NrOfTXPDO"]
        self.lss_supported = dictionary["LSS_Supported"]
        
class EdsDummyUsage(object):
    """docstring for EdsDummyUsage"""
    def __init__(self, dictionary):
        super(EdsDummyUsage, self).__init__()
        # todo figure out semantics
        self.dummy0001 = dictionary["Dummy0001"]
        self.dummy0002 = dictionary["Dummy0002"]
        self.dummy0003 = dictionary["Dummy0003"]
        self.dummy0004 = dictionary["Dummy0004"]
        self.dummy0005 = dictionary["Dummy0005"]
        self.dummy0006 = dictionary["Dummy0006"]
        self.dummy0007 = dictionary["Dummy0007"]

class EdsComments(object):
    """docstring for EdsComments"""
    def __init__(self, dictionary):
        super(EdsComments, self).__init__()
        self.n_lines = int(dictionary["Lines"])
        self.lines = list()
        for k in range(1,self.n_lines+1):
            self.lines.append(dictionary["Line"+str(k)])

def parseIntAutoBase(string):
    if string is None: return None
    if string[:2] == "0x":
        base = 16
    elif string[:2] == "0b":
        base = 2
    else:
        base = 10
    return int(string,base)

class EdsObjectAttribute(Enum):
    #301_v04020005_cor3.pdf pg. 90 
    rw    = 0 # read and write access
    wo    = 1 # write only access
    ro    = 2 # read only access
    const = 3 # read only access, value is constant 
              # The value may change in NMT state Initialisation. 
              # The value shall not change in the NMT states pre-
              # operation, operational and stopped. 
                    

class EdsObjectType(Enum):
    #301_v04020005_cor3.pdf pg. 89 
    null      = 0x00  # object with no data fields
    domain    = 0x02  # large variable amount of data e.g. executable program code 
    deftype   = 0x05  # denotes a type definition such as a BOOLEAN, UNSIGNED16, FLOAT and so on 
    defstruct = 0x06  # defines a new record type e.g. the PDO mapping structure at 21 h  
    var       = 0x07  # A single value such as an UNSIGNED8, BOOLEAN, FLOAT, INTEGER16, VISIBLE STRING etc. 
    array     = 0x08  # A multiple data field object where each data field is a simple variable of the
                      # SAME basic data type e.g. array of UNSIGNED16 etc. Sub-index 0 is of UNSIGNED8 
                      # and therefore not part of the ARRAY data         
    record    = 0x09  # A multiple data field object where the 
                      # data fields may be any combination of 
                      # simple variables. Sub-index 0 is of 
                      # UNSIGNED8 and sub-index 255 is of 
                      # UNSIGNED32 and therefore not part 
                      # of the RECORD data 


class EdsObject(object):
    """docstring for EdsObject"""
    def __init__(self, config_parser, index, subindex = None):
        super(EdsObject, self).__init__()
        object_id_str = str.upper(hex(index)[2:])
        if subindex is not None:
            object_id_str += "sub" + str.upper(hex(subindex)[2:])
            
        dictionary = get_section(config_parser,object_id_str)

        self.index = index
        self.subindex = subindex
        
        self.parameter_name = dictionary["ParameterName"]
        self.object_type = parseIntAutoBase(dictionary["ObjectType"])
        self.obj_flags = dictionary["ObjFlags"]
        
        # object types: (301_v04020005_cor3.pdf pg. 89)
        # 0x00: null - object with no data fields
        # 0x01: null - object with no data fields

        if self.object_type == EdsObjectType.var: 
            # var type
            self.data_type = parseIntAutoBase(dictionary["DataType"])
            self.access_type = dictionary["AccessType"]
            # todo map access_type string to EdsObjectAttribute 
            self.default_value = dictionary["DefaultValue"]
            self.low_limit = parseIntAutoBase(dictionary["LowLimit"])
            self.high_limit = parseIntAutoBase(dictionary["HighLimit"])
            self.pdo_mapping = dictionary["PDOMapping"] == "1"

        elif self.object_type in [EdsObjectType.array, EdsObjectType.record]: 
            assert self.subindex is None # no deep hierarchy
            # array or record type

            # determine number of sub objects
            self.sub_number = int(dictionary["SubNumber"])
            self.sub_objects = list()

            # read sub objects
            for k in range(0,self.sub_number):
                self.sub_objects.append(EdsObject(config_parser, self.index, k))

class EdsObjectList(object):
    """docstring for EdsObjectList"""
    def __init__(self, config_parser, section):
        super(EdsObjectList, self).__init__()

        # get section from eds file
        dictionary = get_section(config_parser,section)

        # retrieve number of objects and then read objects
        self.num_objects = int(dictionary["SupportedObjects"])
        self.object_ids = list()
        self.objects = dict()

        # read objects
        for k in range(1,self.num_objects+1):
            object_id = parseIntAutoBase(dictionary[str(k)])
            self.object_ids.append(object_id)
            self.objects[object_id] = EdsObject(config_parser,object_id)

def get_section(config_parser,section):
    return defaultdict(lambda:None,dict(config_parser.items(section)))

class EdsFile(object):
    def __init__(self):
        '''
        @summary: EDS File loader; describing CanOpen device with supported CanOpen objects
        @result: 
        '''

        super(EdsFile, self).__init__()
        self.config_parser = RawConfigParser()
        self.config_parser.optionxform = str # disable to lower case conversion of option names

        self.file_info = None
        self.device_info = None
        self.dummy_usage = None
        self.comments = None
        self.mandatory_objects = None
        self.optional_objects = None

    def read(self, filename):
        '''
        @summary: reads in eds file from filename
        @param filename: path specifying eds file
        @result: 
        '''

        self.config_parser.read(filename)



        self.file_info = EdsFileInfo(get_section(self.config_parser,"FileInfo"))
        self.device_info = EdsDeviceInfo(get_section(self.config_parser,"DeviceInfo"))
        self.dummy_usage = EdsDummyUsage(get_section(self.config_parser,"DummyUsage"))
        self.comments = EdsComments(get_section(self.config_parser,"Comments"))
        self.mandatory_objects = EdsObjectList(self.config_parser,"MandatoryObjects")
        self.optional_objects = EdsObjectList(self.config_parser,"OptionalObjects")


    # def write(self, filename):
    #     with open(filename, 'wb') as configfile:
    #         self.config_parser.write(configfile)


# __all__ = [EdsFileInfo,EdsDeviceInfo,EdsDummyUsage,EdsComments,EdsObject,EdsObjectList,EdsFile]
