# CvpGetConfigs.py 

The purpose of this script is to pull the running configuration of all switches that are 
managed by CVP through the CVP API. 

# Author
Jeremy Georges 

# Description
CvpGetConfigs

The purpose of this script is to pull the running configuration of all switches that are
managed by CVP through the CVP API.

The main reason behind this script is that several customers have asked if its possible to save the running 
configuration on each switch through the CVP API, perhaps to back these configs up to some repo. 



## CLI Arguments

```
usage: CvpGetConfigs.py [-h] -s SERVER -u USERNAME [-p PASSWORD]

Arguments for script

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        CVP Server IP/HOST
  -u USERNAME, --username USERNAME
                        CVP Username
  -p PASSWORD, --password PASSWORD
                        password
```
 


License
=======
BSD-3, See LICENSE file
