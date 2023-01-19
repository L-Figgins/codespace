from datetime import timezone
import datetime
  
def get_utc_timestamp()-> int:
 
    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)
    
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    return int(round(utc_timestamp))