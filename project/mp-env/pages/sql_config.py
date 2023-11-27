import mysql.connector


def credentials():
    sql_config = {
    "user": "uuvipz0v8e4x2axm",
    "password": "35UW4RDkqBWIy5NfT3Wp",
    "host": "bkzxz5yi2mqoyjhpjzcd-mysql.services.clever-cloud.com",
    "database": "bkzxz5yi2mqoyjhpjzcd",
    "port": "3306"
    }
    
    credentials = mysql.connector.connect(user=sql_config["user"],
                                          password=sql_config["password"],
                                          host=sql_config["host"],
                                          database=sql_config["database"],
                                          port=sql_config["port"])
    
    return credentials


def verify_connector():
    try:
        connector = credentials()
        print(connector) 
    except Exception as error:
        print(error)

def main():
    verify_connector()


if __name__ == "__main__":
    main()