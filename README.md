<h3> How to run the database locally using Docker: </h3> 

- Install Docker
- Make sure Docker is running  
- Run this command to start the container: docker-compose up -d
- Acess the database through this command:  docker exec -it client_info_db -U admin -d client
- Use the terminal to update the tables using psql