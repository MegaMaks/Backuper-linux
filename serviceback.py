from apscheduler.schedulers.background import BackgroundScheduler
import sql_function as sql
import pgdump
import schedule
import time, os
from datetime import datetime, timedelta

def prepare_full_backup(id_server):
        id_task=sql.get_id_task(id_server)
        if id_task > 0:
                task = sql.get_task_settings(id_task)
                scheduler.start()
                if task.exeption == 'psql':
                        scheduler.add_job( pgdump.postgres_backup_database, 'date',run_date=task.next_start, args=[id_task,task])
                        print(id_task)
        else:
                print("not active tasks")


        return task

def tick(text):
        print(text + '! The time is: %s' % datetime.now())

scheduler = BackgroundScheduler()
#dd = datetime.now() + timedelta(seconds=6)
#scheduler.add_job(tick, 'date',run_date=dd, args=['TICK'])

#dd = datetime.now() + timedelta(seconds=6)
#scheduler.add_job(tick, 'date',run_date=dd, kwargs={'text':'TOCK'})

#scheduler.start()
#print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
print(prepare_full_backup(2))

try:
        while True:
                time.sleep(2)
except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
