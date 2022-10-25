## How to build containers

To properly build all the custom containers, you have to:

* API:
''' docker build -t rana_api -f API/Dockerfile

## RUN

In order to run the app you need:

1. First create a bridge network in order to use
2. Create the Mongodb Persistent volume
3. Run Mongodb and Mongo-express containers
4. Run RabbitMQ container
5. Run the backend container
6. Run the API container 
