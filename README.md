# QueryQueens

# Endpoints:
 
+ [] = not optional
+ () = optional

| Endpoint               | Parameters                                                                                         | Return type | Function                                                                                              |
|------------------------|----------------------------------------------------------------------------------------------------|-------------|-------------------------------------------------------------------------------------------------------|
| /api                   | -                                                                                                  | String      | testing                                                                                               |
| /api/test              | -                                                                                                  | String      | testing                                                                                               |
| /api/log/last          | -                                                                                                  | json        | Returns the timestamp of the last POST call                                                           |
| /api/populate          | Uses the preconfig_data.json                                                                       | String      | Filling the database with test data                                                                   |
| /api/product           | /parameters(color=red&size=medium&...)                                                             | json        | Returns all products fitting the given parameters <br/>If none are provided returns all products      |
| /api/cart/add          | **/ProductID[63d88491d129e41e34895dfc] <br/>/amount[int]** <br/>/cart_id(63d0fe458e2f9348609c71f6) | String(ID)  | Adds a Product to a cart <br/>If no ID is provided creates a new cart                                 |
| /api/cart/nuke         | **/cartID[63d0fe458e2f9348609c71f6]**                                                              | String      | Deletes a cart                                                                                        |
| /api/order             | **/cartID[63d0fe458e2f9348609c71f6]** <br/>/data(id=user_id&address=here&whatever=something&....)  | String      | Creates an order from an existing cart<br/>if id is provided in data, imports all data from that user |
| /api/user/create       | **/username[String] <br/>/password[String]**                                                       | String(ID)  | Creates a user and returns the ID                                                                     |
| /api/user/authenticate | **/username[String] <br/>/password[String]**                                                       | String(ID)  | Authenticates a user and returns their ID                                                             |
| /api/user/nuke         | **/userid[63d0fe458e2f9348609c71f6]**                                                              | String      | Removes a user from the database                                                                      |
| /api/user/update       | **/userid[63d0fe458e2f9348609c71f6] <br/>/field[username, password, etc.]=[String]**               | String      | Edits or adds fields to the users data                                                                |
| /api/user/data         | **/username[String]**                                                                              | json        | Returns the user data, without password or ID                                                         |

# Return Codes:

+ 200 = Returned successfully
+ 201 = Created successfully
+ 202 = Deleted successfully
+ 203 = Edited successfully
+ 400 = Bad Request
+ 401 = Not authenticated
+ 403 = Forbidden Request
+ 404 = Not found
+ 409 = Forbidden Request