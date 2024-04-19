


# GOOGLE_SHEETS = "ass-993@orders-418210.iam.gserviceaccount.com"
# TOKEN= 6434993431:AAETBvvvuJrwcHeay900QpJ9Svnwy5bc664
# DATEBASE=mongodb://localhost:27017/
# ADMIN_ID= 9665230060
# MANAGER_ID=""
import os
from dotenv import load_dotenv
print(load_dotenv())
TOKEN=os.getenv("TOKEN")
DATEBASE=os.getenv("DATABASE")
ADMIN_ID=os.getenv("ADMIN_ID")
print(ADMIN_ID)