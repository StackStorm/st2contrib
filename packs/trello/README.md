# Trello Integration Pack

Integration pack that provides support for Trello, an online Task Tracking tool

## Configuration

* `api_key` - User API Key
* `token` - User oAuth Token for R/W Access

Note: Each action in this pack also takes `api_key` and `token` as parameters.
If provided, actions will prefer the runtime credentials over the system provided
credentials.

### Obtaining Credentials
#### API Token

API Token can be retrieved from https://trello.com/app-key while logged into your
account.

#### oAuth Token

To obtain an oAuth token, refer to the documentation at https://trello.com/docs/gettingstarted/#getting-a-token-from-a-user

## Supported Actions
```
+---------------------------+--------+--------------------+------------------------------------------------------+
| ref                       | pack   | name               | description                                          |
+---------------------------+--------+--------------------+------------------------------------------------------+
| trello.add_board          | trello | add_board          | Create a new board                                   |
| trello.add_card           | trello | add_card           | Add a new card to a list                             |
| trello.add_list           | trello | add_list           | Add a new list to a board                            |
| trello.close_board        | trello | close_board        | Close a board                                        |
| trello.close_card         | trello | close_card         | Close a card                                         |
| trello.close_list         | trello | close_list         | Close a list belonging to a board                    |
| trello.find_board_by_name | trello | find_board_by_name | Lookup a board ID based on name. Returns one or more |
|                           |        |                    | IDs                                                  |
| trello.find_card_by_name  | trello | find_card_by_name  | Lookup a Card ID based on name. Returns one or more  |
|                           |        |                    | IDs                                                  |
| trello.find_list_by_name  | trello | find_list_by_name  | Lookup a list ID based on name. Returns one or more  |
|                           |        |                    | IDs                                                  |
| trello.move_card          | trello | move_card          | Move a card from one board/list to another           |
|                           |        |                    | board/list                                           |
| trello.view_boards        | trello | view_boards        | Return a dictionary of all boards and their IDs      |
| trello.view_cards         | trello | view_cards         | View all cards on a board                            |
| trello.view_lists         | trello | view_lists         | View all lists belonging to a board                  |
| trello.view_organizations | trello | view_organizations | List all organizations for user                      |
+---------------------------+--------+--------------------+------------------------------------------------------+
```
