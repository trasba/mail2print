# mail2print

mail2print is a Python project to load emails and print their attachments ona physical printer

## Prerequisites

see pyproject.toml

## Installation

use poetry
``poetry install``

## Usage

- adjust config.json

  ```json
    {
        "imap_server":"imap.domain.com",
        "username":"mail@domain.com",
        "password":"12345678",
        "printer":"printer123",
        "folder_path":"/tmp",
        "filter":
        [
            "OR (HEADER FROM domain) (HEADER FROM user)",
            "UNSEEN"
        ]
    }
  ```  

> Most should be self explainatory,  
> **filter** can be a logical expression where OR operations are explicitly written while AND operations are performed between all elemens of the list  
e.g. the given example means, ```UNSEEN AND ((from domain) OR (from user))``` where domain/user will be matched against ```John Doe <j.doe@domain.com>```  
So john would match even though it is not part of the email address.
filter is case-insensitive

- run mail2print.py

``poetry run mail2print``

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)