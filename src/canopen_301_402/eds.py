#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict
from ConfigParser import RawConfigParser, NoSectionError
from flufl.enum import Enum

from canopen_301_402.utils import parseIntAutoBase

from canopen_301_402.constants import *


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



class EdsObject(object):
    """docstring for EdsObject"""
    def __init__(self, config_parser, index, subindex = None):
        super(EdsObject, self).__init__()
        object_id_str = str.upper(hex(index)[2:])
        if subindex is not None:
            object_id_str += "sub" + str.upper(hex(subindex)[2:])
        
        try:
            dictionary = get_section(config_parser,object_id_str)
            self.valid = True
            self.index = index
            self.subindex = subindex
            self.datatype = None
            self.default_value = None

            self.parameter_name = dictionary["ParameterName"]
            if dictionary["ObjectType"] is None:
                # Missing  ObjectType  equals  ObjectType  VAR. (306_v01030000.pdf pg. 15)
                self.object_type = CanOpenObjectType.var
            else:
                self.object_type = parseIntAutoBase(dictionary["ObjectType"])
                self.object_type = CanOpenObjectType(self.object_type)
            
            if dictionary["ObjFlags"] is None:
                self.obj_flags = 0
            else:
                self.obj_flags = dictionary["ObjFlags"]
            
            # object types: (301_v04020005_cor3.pdf pg. 89)
            # 0x00: null - object with no data fields
            # 0x01: null - object with no data fields
            if self.object_type == CanOpenObjectType.var:
                # var type
                self.datatype = parseIntAutoBase(dictionary["DataType"])
                self.access_type = dictionary["AccessType"]
                # todo map access_type string to CanOpenObjectAttribute 
                # 306_v01030000.pdf pg. 15
                # AccessType for this object, represented by  the  following  strings  ( „ro“ - read  only,  „wo“ -
                # write  only,  „rw“  -  read/write,  „rwr“  -  read/write  on  process  input,  „rww“  -
                # read/write on process output, „const“ - constant value)
                
                try:
                    enum_datatype = CanOpenBasicDatatypes(self.datatype)
                except ValueError:
                    enum_datatype = self.datatype


                if dictionary["DefaultValue"] is None:
                    self.default_value = None
                elif enum_datatype == CanOpenBasicDatatypes.vis_str:
                    self.default_value = dictionary["DefaultValue"]
                elif enum_datatype in [CanOpenBasicDatatypes.boolean,
                                       CanOpenBasicDatatypes.int8,
                                       CanOpenBasicDatatypes.int16,
                                       CanOpenBasicDatatypes.int32,
                                       CanOpenBasicDatatypes.uint8,
                                       CanOpenBasicDatatypes.uint16,
                                       CanOpenBasicDatatypes.uint32]:

                    if "$NODEID" in str.upper(dictionary["DefaultValue"]):
                        self.default_value = dictionary["DefaultValue"] # todo parse this
                    else:
                        self.default_value = parseIntAutoBase(dictionary["DefaultValue"])
                elif enum_datatype == CanOpenBasicDatatypes.float32:
                    self.default_value = float(dictionary["DefaultValue"])
                
                self.low_limit = parseIntAutoBase(dictionary["LowLimit"])
                self.high_limit = parseIntAutoBase(dictionary["HighLimit"])
                self.pdo_mapping = dictionary["PDOMapping"] == "1"

                if self.subindex is None:
                    self.subindex = 0


            elif self.object_type in [CanOpenObjectType.array, CanOpenObjectType.record]: 
                # array or record type

                # determine number of sub objects
                self.sub_number = int(dictionary["SubNumber"])
                self.sub_objects = list()

                # read sub objects
                for k in range(0,self.sub_number+1):
                    self.sub_objects.append(EdsObject(config_parser, self.index, k))
            

        except NoSectionError:
            self.valid = False


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
        self.manufacturer_objects = None
        self.optional_objects = None

        self.objects_by_name = dict()

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
        self.manufacturer_objects = EdsObjectList(self.config_parser,"ManufacturerObjects")

        self.objects_by_name = dict()
        self._add_objects_to_dict(self.mandatory_objects)
        self._add_objects_to_dict(self.optional_objects)
        self._add_objects_to_dict(self.manufacturer_objects)

    def _add_objects_to_dict(self, object_list):
        for obj in object_list.objects.itervalues():
            if obj.valid:
                self.objects_by_name[obj.parameter_name] = obj
                if hasattr(obj,"sub_objects"):
                    for subobj in obj.sub_objects:
                        if subobj.valid:
                            self.objects_by_name[subobj.parameter_name] = subobj

    def get_object(self, index, subindex):
        # print hex(index), hex(subindex)

        def get_object_from_object_list(object_list):
            if object_list is not None:
                if index in object_list.objects:
                    obj = object_list.objects[index]
                    if hasattr(obj,"sub_objects"):
                        return obj.sub_objects[subindex]
                    else:
                        return obj

        result = get_object_from_object_list(self.mandatory_objects)
        if result is None:
            result = get_object_from_object_list(self.optional_objects)
            if result is None:
                result = get_object_from_object_list(self.manufacturer_objects)

        return result

    # def write(self, filename):
    #     with open(filename, 'wb') as configfile:
    #         self.config_parser.write(configfile)


# __all__ = [EdsFileInfo,EdsDeviceInfo,EdsDummyUsage,EdsComments,EdsObject,EdsObjectList,EdsFile]
