from openai import OpenAI
import os
import dotenv
import time
dotenv.load_dotenv()
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
client = OpenAI(
    api_key=OPENAI_API_KEY
)

file=client.files.create(
  file=open("mydata.jsonl", "rb"),
  purpose="fine-tune"
)

fine_tuning_job=client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-3.5-turbo-1106"
)
job_id=fine_tuning_job.id
while True:
    job_status = client.fine_tuning.jobs.retrieve(job_id).status
    job_details = client.fine_tuning.jobs.retrieve(job_id)
    if job_status == "succeeded":
        print("Successful!")
        print(job_details)
        break
    elif job_status == "failed":
        print("Failed, please try again")
        print(job_details.error)
        break
    else:
        print(f"State:{job_status}，wait")
        time.sleep(10) # 等待10秒后再查询任务状态

if job_status == "succeeded":
    new_model_id = client.fine_tuning.jobs.retrieve(job_id).fine_tuned_model
    organization_id=client.fine_tuning.jobs.retrieve(job_id).organization_id
    new_model_name = client.models.retrieve(new_model_id).name
    print(f"Name of new model:{new_model_name}。")

