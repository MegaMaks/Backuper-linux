import sql_function
import mics
import os
import classes as cs
from cmd import Cmd
from pathlib import Path

### FUNCTIONS ###

def display_title_bar():
    os.system('clear')
              
    print("\t**********************************************")
    print("\t**  Backuper for Linux dev Itmix Group ltd  **")
    print("\t**********************************************")  

def get_init_choice():
    print("\n[1] Add a new organixation.")
    print("[2] Select organization")
    print("[q] Quit.")
    
    return input("Select the desired memu item: ")

def get_task_choice():
    print("\n[1] Add database backup task PostgreSQL .")
    print("[2] Add database backup task MySQL(MariaDB)")
    print("[3] Add full backup task files and dirs")
    print("[4] Add differencial backup task file and dirs")
    print("[5] Show currents backup tasks")
    print("[q] Quit.")
    
    return input("Select the desired menu item: ")

def init_server():
  
  choice = ''
  while choice != 'q':    
    
    choice = get_init_choice()
    display_title_bar()
    
    if choice == '1':
        name_org = input("Input name of organizatin: ")
        id_org = sql_function.add_org(name_org,4)
        print ("Id organization: " + id_org)
        name_server = input("Enter name of the server: ")
        server_ip = input("Enter IP adress: ")
        id_server = sql_function.add_server(name_server,server_ip,id_org)
        print ("Id server: " + id_server)
        file = open("serverid", "w")
        file.write(id_server)
        file.close()
        create_task(id_server)

    elif choice == '2':
        print("\nList of existing organization\n")
        dict_org = sql_function.show_org(4)

        for key in dict_org:
            print("%s - %s" %(key, dict_org[key]))

        id_org = input("Input id necessary organizatin: ")
        dict_server = sql_function.show_servers(id_org)
        display_title_bar()
        print("\nList of existing servers in %s organization\n"%(dict_org[id_org]))
        
        for key in dict_server:
            print("%s - %s" %(key, dict_server[key]))
        id_server = input("Input id necessary server: ")
        file = open("serverid", "w") 
        file.write(id_server) 
        file.close()
        create_task(id_server)
    elif choice == 'q':
        print("\nThanks for playing. Bye.")
    else:
        print("\nI didn't understand that choice.\n")

def create_task(id_server):
  choice = ''
  while choice != 'q':

    choice = get_task_choice()
    display_title_bar()
    if choice == '1': 
         task_name = input("Input name of task: ")
         pg_user = input("Input postgreSQL username:[postgres] ")
        
         if pg_user=="":
             pg_user="postgres"
         print("\nList of existing databases\n")
         get_database_info(pg_user)
         source = input("Enter a comma-separated [,] list of required databases: ")
         dest = input("Enter a destination path: ")
         sel_day = input("Enter days of the week when to run a task: ")
         task_time = input("Enter time when to run a task: example 22:00:00 ")
         next_start = mics.get_next_time(sel_day, task_time)
         time_live = input("Enter the number of days to store the backup: ")
         extension = "zip"
         password = pg_user
         exeption = "psql"
         task = cs.Task(task_name,source,dest,sel_day,task_time,id_server,next_start,time_live,extension,password,exeption)
         sql_function.add_full_task(task)
         print("\nTask successfully added, next start time at %s\n" %next_start)
    elif choice == '2':
         print("\nThanks for playing. Bye.")

def get_database_info(user):   
    return os.system('psql -E -U {} -c "\l"'.format(user))

### MAIN PROGRAM ###

display_title_bar()
serverid = Path("./serverid")
if serverid.is_file():
   f = open(serverid, "r")
   create_task(f.read()) 
   f.close() 
   #print("Hello world")
else:
   init_server()
