[TagToEquip]
by Robert Sims
project to convert tags in citect to a hierachical tree struture (Equipment)

- supports .csv files
- supports .dbf file if project is in user directory and user directory is same level as config directory
- supports user defined mapping trough mapping.ini
- outputs *-working.csv files under files path attribute given which can be imported into project using Citect Studio

[source code]
https://github.com/robmsims/TagToEquip-Python

[useage]
>Main-import-variables.exe {path}    --> will create a mapping file: maapping.ini under {path}
 --on 2nd run 
>Main-import-variables.exe {path}    --> read in mapping.ini under {path} and create *-working.csv files containing                                          equipment field changes which can be imported into project using Citect Studio import

[args]
{path} is location of master (root) project ie C:\ProgramData\Schneider Electric\Citect SCADA 2018\User\Example

[history]
ported to python from originaly cicode version
upgraded to write back to csv file
upgraded to support mapping file
upgraded to create source .csv files from master project .dbf and include projects

[source code]
https://github.com/robmsims/TagToEquip-Python