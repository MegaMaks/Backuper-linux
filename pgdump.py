import gzip
import classes
import sql_function as sql
import datetime
from sh import pg_dump
#def postgres_backup_database(user,database,path,id_task):
def postgres_backup_database(id_task,task):
        date_backup = datetime.datetime.now()
        databases=task.source.split(",")  
        status = "success"
        for db in databases:
                db = db.strip()
                current_path = task.dest + date_backup.strftime("%d-%m-%Y_%H-%M-%S-") + db + ".gz"
                try:
                    with gzip.open(current_path, 'wb') as f:
                        pg_dump('-U', task.password, db, _out=f)
                except Exception as e:
                    status = "backup failed: " + str(e)
        if status == "success":
                sql.add_task_log(id_task,"Завершено успешно: " + task.source,1 )
        else:
                sql.add_task_log(id_task,status.encode('utf8'),0 )
#status = postgres_backup_database('postgres',' tms , ttt ','/mnt/backup/')
#print(status)
