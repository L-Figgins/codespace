from datetime import timezone
import datetime
import uuid
  
def get_utc_timestamp()-> int:
 
    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)
    
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    return int(round(utc_timestamp))

def generate_user_id()-> str:
    """
    Generate a random UUID using uuid4
    """
    return uuid.uuid4()

