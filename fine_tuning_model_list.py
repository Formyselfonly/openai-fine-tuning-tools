from openai import OpenAI
import os
import dotenv
import datetime
import time
dotenv.load_dotenv()
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
client = OpenAI(
    api_key=OPENAI_API_KEY
)


# 列出所有微调任务
jobs = client.fine_tuning.jobs.list()
# 获取每个微调任务的fine_tuned_model名称
for job in jobs:
    fine_tuned_model_id = job.fine_tuned_model
    training_file_id=job.training_file
    training_file=client.files.retrieve(training_file_id)
    training_create_time=training_file.created_at
    training_create_time = datetime.datetime.fromtimestamp(training_create_time).strftime('%Y-%m-%d %H:%M:%S')
    training_file_json_name=training_file.filename

    print(f"Fine-tuned model name: {fine_tuned_model_id},Training file:{training_file_json_name},Training create time:{training_create_time}")


