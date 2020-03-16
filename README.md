#       TagToEquip-Python
## project to convert tags in citect to a hierarchical tree structure (Equipment)
### - supports .csv files
### - supports .dbf file if project is in user directory and user directory is same level as config directory
#### --- Note: uses 3rd party library https://pypi.org/project/dbf/
### - supports user defined mapping trough mapping.ini
### - outputs *-working.csv files under files path attribute given which can be imported into project using Citect Studio
#### - Todo. add log output of scores for first area detection. Is equip type unique for area digit value, is digit value uniquw for equipp type
#### - Todo. expose scoring algorithm in to a config file so it can be tuned by users.

## [useage]
#### python3  Main-import-variables {path}    --> will create a mapping file: maapping.ini under {path}
#### --on 2nd run 
#### python3  Main-import-variables {path}    --> read in mapping.ini under {path} and create *-working.csv files containing equipment field changes which can be imported into project using Citect Studio import

## [args]
#### {path} is location of master (root) project ie C:\ProgramData\Schneider Electric\Citect SCADA 2018\User\Example

### [history]
#### ported to python from originaly cicode version
#### upgraded to write back to csv file
#### upgraded to support mapping file
#### upgraded to create source .csv files from master project .dbf and include projects
#### fix Item generation
#### add Item friendly name mapping
#### fix area mapping. now will only use perfix if area does not have a friendly name assigned