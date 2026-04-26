import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow

# 🔴 Replace with your actual blog ID locally
BLOG_ID = "YOUR_BLOG_ID"

# 🔐 Auth (requires credentials.json locally – DO NOT upload it)
flow = flow_from_clientsecrets(
    "credentials.json",
    scope="https://www.googleapis.com/auth/blogger"
)

storage = Storage("token.json")
creds = storage.get()

if not creds or creds.invalid:
    creds = run_flow(flow, storage)

service = build("blogger", "v3", credentials=creds)

# 📂 Load blogs
with open("blogs.json", "r", encoding="utf-8") as f:
    blogs = json.load(f)

# 🚀 Upload loop
for blog in blogs:
    while True:
        try:
            service.posts().insert(
                blogId=BLOG_ID,
                body={
                    "title": blog["title"],
                    "content": blog["content"]
                },
                isDraft=True
            ).execute()

            print("Uploaded:", blog["title"])
            time.sleep(5)
            break

        except HttpError as e:
            if e.resp.status == 429:
                print("Rate limit hit. Waiting...")
                time.sleep(20)
            else:
                print("Error:", e)
                break