from datetime import datetime, timedelta
x = str(datetime.now()+timedelta(hours=5))[11:19]
print(x)