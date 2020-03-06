# TagToEquip-Python
Python version TagToEquip
## supports csv files
## supports dbf file ifproject is in user directory and user directory is same level as config directory
## outputs *-working.csv files under files path attribute given which can be imported into project using Citect Studio

### useage
>python3  Mail-import-variables {path}    --> will create a mapping file: maapping.ini under {path}
>python3  Mail-import-variables {path}    --> on 2nd run will read in mapping.ini and create *-working.csv files under files path                                                       attribute given which can be imported into project using Citect Studio
### args
{path} is location of master (root) project ie C:\ProgramData\Schneider Electric\Citect SCADA 2018\User\Example

