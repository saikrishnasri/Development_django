from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='python /home/apptrinity10/development/core-python/web_scraper/drink_coaster.py')
job.minute.every(5)

cron.write()
