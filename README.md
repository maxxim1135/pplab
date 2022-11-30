# pplab

Левицький Максим, варіант 7


# deployment 
    Download project and after that it would be easy to open with PYCHARM IDE

    Choose python poetry interpreter upper 3.7.6 if PYCHARM haven't done it already   

    Run command:
    poetry update
    poetry shell   - creating virtual environment
    
    run app.py
    So, Flask server is working now  
    
    If failed with poetry, deleting and rewriting poetry might helt (for me it helped once) 

# database setting
    
    You should enter databese connection info in alembic.ini file
    For example:
    sqlalchemy.url = mysql://user:password@localhost:3306/mydb

    And paste it also in 10 line in params of create_engine function in models.py


    Command to migrate database on your own 

    alembic upgrade head  
    
    Or if you haven't any file in alembic/versions/

    alembic revision --autogenerate -m "Create models"
    alembic upgrade head   

# Commands 
    
    Link to commands list via postman

    All method are written in app.py, database model in models.py, 
    methods schemas in schemas.py and there are also some util files

# Authorization
    
    Basic_auth is used. 

    Admin can be created manually setting appropriate param isAdmin = True.
    All users can be created via standart post method. 
    Admins can post, change and delete audience. Users can only get information about it.

    Users can retrieve from get method informartion only about themselves, update only themselves
    and delete as well.
    It can be modified for need.
