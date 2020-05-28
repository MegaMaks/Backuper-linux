#!/usr/bin/env python
import databaseconfig as cfg
import mics
import classes as cs
import pypyodbc
import datetime
from datetime import datetime

def add_org(name_org,id_client):
        
        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        cursor.execute("EXEC add_org @name_org = ?, @id_Client = ?",(name_org,id_client))
        connection.commit()
        SQLCommand = ("SELECT TOP 1 * FROM Org ORDER BY ID_Org DESC")

        cursor.execute(SQLCommand)
        rowCount = 0

        for row in cursor:
             rec =  str(row[0])

        cursor.close()
        connection.close()
        return rec
def add_server(server_name,server_ip,id_org):

        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        cursor.execute("EXEC add_server @server_name = ?,@server_ip = ?,@id_org = ?",(server_name,server_ip,id_org))
        connection.commit()
        SQLCommand = ("SELECT TOP 1 * FROM server ORDER BY ID_server DESC")

        cursor.execute(SQLCommand)
        rowCount = 0

        for row in cursor:
             rec =  str(row[0])

        cursor.close()
        connection.close()
        return rec

def add_full_task(task):

        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        cursor.execute("EXEC add_full_copy @task_name = ?,@source = ?,@dest = ?,@sel_day = ?,@task_time = ?,@id_server = ?,@next_start = ?,@time_live = ?,@extension = ?,@password = ?,@date_add = ?,@ftp = 0,@exeption = ?,@shadow = 0",(task.task_name,task.source,task.dest,task.sel_day,task.task_time,task.id_server,task.next_start,task.time_live,task.extension,task.password,datetime.today().strftime('%Y-%m-%d'),task.exeption))
        connection.commit()

        cursor.close()
        connection.close()

def add_task_log(id_task,log,status):

        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        cursor.execute("EXEC add_full_log @task_log = ?, @datelog = ?,@id_task = ?,@success = ? ",(log,datetime.today(),id_task, status))
        connection.commit()

        cursor.close()
        connection.close()

def show_org(id_client):

        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        cursor.execute("EXEC sel_org @id_Client = ?",[id_client])
        rowCount = 0
        org_dict = dict()
        for row in cursor:
                org_dict[str(row[0])]=str(row[1])
                rowCount = rowCount + 1

        cursor.close()
        connection.close()
        return org_dict

def show_servers(id_org):

        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        SQLCommand = ("Select id_server,Server_name,server_IP from server where status=1 and id_org =?")
        cursor.execute(SQLCommand,[id_org])
        rowCount = 0
        server_dict = dict()
        for row in cursor:
                server_dict[str(row[0])]=str(row[1])
                rowCount = rowCount + 1

        cursor.close()
        connection.close()
        return server_dict

def get_id_task(id_server):
        try:
                while True:
                        connection = pypyodbc.connect(cfg.connection_string)
                        cursor = connection.cursor()
                        SQLCommand = ("Select TOP 1 id_task,next_start,sel_day,task_time from task where id_server =? and status=1 order by (next_start)")
                        cursor.execute(SQLCommand,[id_server])
                        for row in cursor:
                                id_task =  row[0]
                                next_start = row[1]
                                get_days = row[2]
                                task_time = row[3]
                           
                        cursor.close()
                        connection.close()
                        result_compare = datetime.now() > next_start
                        if result_compare:
                                update_next_start(id_task, get_days, task_time)
                        else:
                                break

                return id_task
        except Exception:
                return 0

def update_next_start(id_task, get_days, task_time):
        next_start = mics.get_next_time(get_days,task_time.strftime('%H:%M:%S'))
        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        SQLCommand = ("update task set next_start =? where id_task =?")
        cursor.execute(SQLCommand,[next_start,id_task])
        connection.commit() 
        cursor.close()
        connection.close()


def get_task_settings(id_task):
        connection = pypyodbc.connect(cfg.connection_string)
        cursor = connection.cursor()
        SQLCommand = ("Select * from task where id_task =?")
        cursor.execute(SQLCommand,[id_task])
        for row in cursor:
                task = cs.Task(row[1],row[2],row[3],row[6],row[7],row[9],row[5],row[11],row[12],row[13],row[16])
         
        cursor.close()
        connection.close()
        return task
              


