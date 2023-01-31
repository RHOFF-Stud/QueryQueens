# QueryQueens

# Endpoints:
 
+ [] = not optional
+ () = optional

| Endpoint               | Parameters                                                                                         | Return type | Function                                                                                         |
|------------------------|----------------------------------------------------------------------------------------------------|-------------|--------------------------------------------------------------------------------------------------|
| /api                   | -                                                                                                  | String      | testing                                                                                          |
| /api/test              | -                                                                                                  | String      | testing                                                                                          |
| /api/log/last          | -                                                                                                  | json        | Returns the timestamp of the last POST call                                                      |
| /api/populate          | Uses the preconfig_data.json                                                                       | String      | Filling the database with test data                                                              |
| /api/product           | /parameters(color=red&size=medium&...)                                                             | json        | Returns all products fitting the given parameters <br/>If none are provided returns all products |
| /api/cart/add          | **/ProductID[63d0fe458e2f9348609c71f4] <br/>/amount[int]** <br/>/cart_id(63d0fe458e2f9348609c71f6) | String      | Adds a Product to a cart <br/>If no ID is provided creates a new cart                            |
| /api/cart/nuke         | **/cartID[63d0fe458e2f9348609c71f6]**                                                              | String      | Deletes a cart                                                                                   |
| /api/order/guest       | **/cartID[63d0fe458e2f9348609c71f6]** <br/>/data(String)                                           | String      | Creates an order from an existing cart as a guest user                                           |
| /api/order/user        | **/cartID[63d0fe458e2f9348609c71f6] <br/>/userid[63d0fe458e2f9348609c71f6]**                       | test        | testing                                                                                          |
| /api/user/create       | **/username[String] <br/>/password[String]**                                                       | test        | testing                                                                                          |
| /api/user/authenticate | **/username[String] <br/>/password[String]**                                                       | test        | testing                                                                                          |
| /api/user/nuke         | **/userid[63d0fe458e2f9348609c71f6]**                                                              | test        | testing                                                                                          |
| /api/user/update       | **/userid[63d0fe458e2f9348609c71f6] <br/>/username(String) <br/>/password(String)**                | test        | testing                                                                                          |
| /api/user/data         | **/username[String]**                                                                              | test        | testing                                                                                          |

# Return Codes:

+ 200 = Returned successfully
+ 201 = Created successfully
+ 202 = Deleted successfully
+ 400 = Bad Request
+ 401 = Not authenticated
+ 403 = Forbidden Request
+ 404 = Not found
+ 409 = Forbidden Request