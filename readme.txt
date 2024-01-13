README:

Instruction on how to use the project:

Recover the database (Postgres SQL 15.4) with one of the 3 sql file.
Recommendation is to use tar file or custom file and restore via pgAdmin4 (8.1) with UTF-8 encoding, role of postgres
(password for user postgres is admin, if your password is different please change accordingly inside IMDB.py in the functions that use psycopg2.connect())
database name must be IMDB_INFO to be compatible with the code, or must be modified in IMDB.py for functions that use psycopg2.connect()

Once data is recovered install all dependencies as per the import. The python version as tested working is 3.12.1
Run python3 main.py

venv virtual enviroment may need to be deleted then reinstalled, or you can decide to run without virtual enviroment