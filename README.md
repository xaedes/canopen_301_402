
Implementation of necessary subset of CanOpen 2.a to control Faulhaber Motion Controller.

Implemented Features:
 - Network Management (controlling the Can301 State Machine)
 - SDO expedited transfer
 - EDS file loading
 - PDO transfer
 - CanOpen StandardDataTypes
 - generic pre-defined connection set (301_v04020005_cor3.pdf pg. 86)
 - 402 StateMachine

Todo:
 - 402:
   - Node
   - read current state
   - Read available Motion Profiles
   - Set Motion Profile

 - PDO mapping (301_v04020005_cor3.pdf pg. 93; 135; 139 for transmission type)
 - complete object dictionary dump and restore
 - Sync Message (to trigger pdo)
 - use contents in EDS file (but how o0)

 


Not that important todos:
 - respect inhibit times (specified as multiples of 100 microsec)
 - local object dictionary prepopulated with can standard defaults
   - could be used to implement a can master (device)
 - datatypes in object dictionary (301_v04020005_cor3.pdf pg. 88)
 - datatype coding with datatype info in object dictionary

 - sdo block transfer
 - specific connection-set 
   - overwrite standards with values in eds file
   - respect restricted CAN-IDs  (301_v04020005_cor3.pdf pg. 87)

 - print canopen frame in human readable form (we can use EDS file for this)