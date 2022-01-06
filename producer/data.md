# Data
There are two sets of static datasets, users and articles, and one dynamic dataset that is created continuously.

## Static data
The static data is created by `users.py` and `articles.py`, user data as well as product data.
These two data sources are "clean" and are available in two formats, both as files (one file per record in the `blob/article` & `blob/user` directory) as well as in the tables `articles` and `users` in the postgres database `database`.

### Users
Customer information, with unique `id_`.
Each purchase event needs to include a `user_id` that is represented in `users`.

| Column | Description |
| -------- | ------------- |
| `id_` | UUID4. |
| `name` | Name of the user. |
| `address` | A fake address. |
| `number` | Phone number. |
| `email` | Email |

*In real life it is very unlikely that we would process sensitive user information like this...*

### Articles
Product information, with unique `id_`.
Each purchase event needs to include an `article_id` that is represented in `articles`.

| Column | Description |
| -------- | ------------- |
| `id_` | UUID4. |
| `name` | Name of the product (randomly generated...). |
| `price` | The price of the product. |
| `currency` | The currency. |

## Dynamic data
The data that is produced continously is purchase event data, i.e. data with timestamps of when a specific user made a purchase of specific articles.
This data is not yet validated and may be broken.
It might contain `article_id`'s or `user_id`'s that are not represented in the users/articles, or broken attributes.
This is the data to validate and clean, and store in a queryable format.

| Column | Description |
| -------- | ------------- |
| `id_` | UUID4. |
| `timestamp` | Name of the product (randomly generated...). |
| `user_id` | The price of the product. |
| `cart` | List of {`article_id`: <>, `quantity`: <>}. |

This data is available to consume in two different ways, you can chose to use either/both:
 1. json files dumped in `blob/purchases`
 2. events published to the `pubsub` service, exposed to the port `8085`
