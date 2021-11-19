# To use Makefile commands, you need to install "make"  https://qastack.ru/programming/32127524/how-to-install-and-use-make-in-windows
# Also You can just copy and paste this commands to terminal
# This command runs new docker container with database. Use it when you broke old db container. Example: make run
run:
	docker run --name enrollment_assistant -e POSTGRES_DB=enrollment_assistant -e POSTGRES_USER=developer -e POSTGRES_PASSWORD=passdev -p 5432:5432 -v PGDATA:/var/lib/postgreqsql/data -d postgres:13.4-alpine

# This command starts existing docker container with database. Use it every time you want to start working with project
start:
	docker start enrollment_assistant
# This command stops existing docker container.
stop:
	docker stop enrollment_assistant

# This command deletes existing docker container.
delete:
	docker rm enrollment_assistant
