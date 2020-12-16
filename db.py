"""
    have to manually connect to root localhost and create another user to whom you will connect here
"""

import pymysql


  $users = "CREATE TABLE `users` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `username` VARCHAR(50) NOT NULL,
        `mail` VARCHAR(100) NOT NULL,
        `password` VARCHAR(255) NOT NULL,
        `token` VARCHAR(50) NOT NULL,
        `verified` VARCHAR(1) NOT NULL DEFAULT 'N'
    )";

    $artgallery = "CREATE TABLE `gallery` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `userid` INT(11) NOT NULL,
        `img` VARCHAR(100) NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(id)
      )";

    $like = "CREATE TABLE `like` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `userid` INT(11) NOT NULL,
        `galleryid` INT(11) NOT NULL,
        `type` VARCHAR(1) NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(id),
        FOREIGN KEY (galleryid) REFERENCES gallery(id)
      )";

    $comment = "CREATE TABLE `comment` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `userid` INT(11) NOT NULL,
        `galleryid` INT(11) NOT NULL,
        `comment` VARCHAR(255) NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(id),
        FOREIGN KEY (galleryid) REFERENCES gallery(id)
      )";




























# Function for connecting to MySQL database sudo pip install setuptools --upgrade
def mysqlconnect(): 
    #Trying to connect  
    dbh = None
    try: 
        dbh = pymysql.connect("localhost","student","0000", "elevage") #last is the chosen database that belongs to user, 2nd is user, 1st server location, 3rd password
    # If connection is not successful 
    except Exception as e: 
        
        print(f"Can't connect to database manager root : {e}") 
        return 0
    # If Connection Is Successful 
    #dbh.rollback()
    print("Connected to user") 

    # Making Cursor Object For Query Execution 
    cursor=dbh.cursor() 
    print(cursor)
    # Executing Query 
    try:
        """INSERT INTO (FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
        #cursor.execute("INSERT ")
        # cursor.execute("CREATE USER 'testX'@'localhost' IDENTIFIED BY '0000'") 
        #cursor.execute("GRANT ALL PRIVILEGES ON elevage.* TO 'testX'@'localhost'") 
        #dbh.commit()
    
    except:
   # Rollback in case there is any error
        dbh.rollback() #rewind action
    

    """
    # Above Query Gives Us The Current Date 
    # Fetching Data  
    m = cursor.fetchone() 

    # Printing Result Of Above 
    print("Today's Date Is ",m[0]) 
    """
    # Closing Database Connection  
    dbh.close()
    print(f'closed db connection : {dbh} !')
    
  
# Function Call For Connecting To Our Database 
mysqlconnect()
