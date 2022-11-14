# SMApply Tools

This repo contains an API library to connect to the SM Apply API and do the following actions:
 - List applications
 - Get details of one application

## Getting Started

### Prerequisites

* Python 3.6 or later - [found here](http://www.python.org/getit/)
* You will also need a [SM Apply Access token](https://connect.smapply.io/pages/authentication.html)

### Setting up the config files

In the `config/` folder there is a config files:

#### **smapply.cfg**

This file is used to set up your credentials to SM Apply. To be able to connect to SM Apply, you will need the base URL to the SM Apply instance, as well as a Access Token. 

1. **URL = *https://example.smapply.com***

   * This is the URL to your SM Apply site

2. **BEARER = *access_token***

   * This will be the [SM Apply Access token](https://connect.smapply.io/pages/authentication.html).

3. **DEFAULT_PROGRAM_ID = *12345***

   * This is the ID of the program you want to be the default program users are enrolled in.

*Remember that your Access Token should be protected the same way you protect a password.*

---

## Running the script


To list all applications:
```
python3 smapply_tools.py list
```
or, if you want to get details on one application
```
python3 standing_deferred.py get APPLICATION_ID
```

## Authors

* **Guillaume Morini** - [GuillaumeMorini](https://github.com/GuillaumeMorini)

## Special thanks

* **Tyler Cinkant** - [lannro](https://github.com/lannro) (https://github.com/ubc/smapply-api)
