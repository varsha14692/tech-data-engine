# Jayway data engineering assignment
## Expectations and delivery
### Your strengths
The assignment has many possible aspects to it and there is no specific requirements on how you solve it.
We hope that you can chose an angle/technology that suits your experience and show us a little of what you know within it.
### Time
We fully respect that everyone has different amount of available time for an assignment like this.
Please do your best with the time you have available, but please share with us roughly how much time you have spent on the assignment

### Document your progress
We are most interested in how you reason about this assignment, more than the actual technical delivery.
Therefore we ask you to your thoughts and struggles down in the file [`progress.md`](progress.md).

### Delivery
When working on this assignment, create your own private repository that you commit to.
When you are finished, please share a link to this repository.
We will let you know which reviewers (github users) we would like for you to share this repository with.
## Goal
A global retail client approaches us (Devoteam) to improve their purchase data processing.
In order to do this you need to build a pipeline consolidating the various data sources, and transform the data so that the purchase data is in quality condition when it reaches the client.

The end goal is **to have validated and clean purchase data in a queryable format**, e.g. in a database.

To solve this you need to consider things like:
 * validating data
 * batch vs stream processing
 * how to add new services to docker-compose
 * how to store the valid data
 * how to handle invalid data

It is suggested to look in the `docker-compose.yml` file to understand how the services are linked.
Also, to better understand the structure of the data, look in `producer/src`.

## Setup
To get this project running, you only need to have [`docker-compose`](https://docs.docker.com/compose/install/) installed on your machine.
All dependencies of the services in this project are managed by docker.

```sh
# run the services
docker-compose -up
```

## Project structure
```
project
│   README.md
│   docker-compose.yml
│
└───purchase_counter
|       Dockerfile
|       count_purchase_files.sh
│
└───producer
│   │   Dockerfile
│   │   requirements.txt
│   │
│   └───src
│       │   articles.py
│       │   events.py
│       │   main.py
│       │   users.py
│   
└───blob
│   └───articles
│   │
│   └───purchases
│   │
│   └───users
```

## Services
The services that are made available in the `docker-compose.yml` file are:
1. `producer`
2. `purchase_counter`
3. `database`
4. `pubsub`
### Producer
There is one service that produces data, `producer` with all relevant code inside the directory with the same name.
There are two sets of static datasets (`users` and `articles`) and one dynamic dataset (`purchase events`) that is created continuously.

Have a look in [`data.md`](producer/data.md) for more info.

### Purchase counter
This is an example service (`purchase_counter`) that is simply counting the number of files in `blob/purchases` to count the number of purchases.
Use this as a source of inspiration for figuring out how to setup your own service.

### Database
The static `user` and `article` data is available in the postgres database (as well as in the `/blob` file storage).

### Pubsub
The `purchase events` data is published to the emulated PubSub topic, exposed at port `8085` (and is also available in the `/blob` file storage).
## Extra?
If time permits and you have already validated, cleaned and stored the purchase data in a queryable format, the client would like to get some high level aggregate information:
 * most commonly bought articles
 * sales per state
 * total number of sales over time

## Feedback
We are not perfect and are open to feedback.
If there is something in this assignment that you find unclear, or that you think could be improved, please share with us!
