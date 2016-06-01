
Implementation of necessary subset of CanOpen 2.a to control Faulhaber Motion Controller.

Implemented Features:
 - Network Management (controlling the Can301 State Machine)
 - SDO expedited transfer
 - EDS file loading
 - PDO transfer
 - CanOpen StandardDataTypes
 - generic pre-defined connection set (301_v04020005_cor3.pdf pg. 86)

Todo:
 - PDO mapping (301_v04020005_cor3.pdf pg. 93; 135; 139 for transmission type)
 - complete object dictionary dump and restore
 - Sync Message (to trigger pdo)
 - use contents in EDS file (but how o0)

 - 402:
   - 402 StateMachine
   - Read available Motion Profiles
   - Set Motion Profile
 


Not that important todos:
 - respect inhibit times
 - local object dictionary prepopulated with can standard defaults
   - could be used to implement a can master (device)
 - datatypes in object dictionary (301_v04020005_cor3.pdf pg. 88)
 - datatype coding with datatype info in object dictionary

 - sdo block transfer
 - specific connection-set 
   - initialized with generic pre-defined connection set
   - overwrite standards with balues in eds file
   - respect restricted CAN-IDs  (301_v04020005_cor3.pdf pg. 87)
   - we need a connection set class for this that manages this
   - this class shall also be responsible for interpreting can frames into canopen frames
   - for canopen frames we need an enum for services (nmt, sync, pdo, etc.) that does not 
      represent the function code directly (as this can be changed)


ideas from other implementations:

    https://github.com/rscada/libcanopen/blob/master/python/pycanopen/CANopen.py

        read canopen frame:

            def read_can_frame(self):
                """
                Low-level function: Read a CAN frame from socket.
                """
                if self.sock:
                    can_frame = CANFrame()
                    if libc.read(self.sock, byref(can_frame), c_int(16)) != 16:
                        raise Exception("CAN frame read error")
                    return can_frame
                else:
                    raise Exception("CAN fram read error: socket not connected")
                    
            def parse_can_frame(self, can_frame):
                """
                Low level function: Parse a given CAN frame into CANopen frame
                """
                canopen_frame = CANopenFrame()        
                if libcanopen.canopen_frame_parse(byref(canopen_frame), byref(can_frame)) == 0:
                    return canopen_frame
                else:
                    raise Exception("CANopen Frame parse error")

        print canopen frame in human readable form (we can use EDS file for this)