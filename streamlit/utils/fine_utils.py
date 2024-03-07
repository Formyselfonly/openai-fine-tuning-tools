import datetime
import os
import dotenv
import time
from openai import OpenAI
# 加载环境变量
dotenv.load_dotenv()

class fine_utils_API():
    ""
    
    def __init__(self):
        # 获取 OPENAI_API_KEY
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

        # 初始化客户端
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        
    
    def chat_Models(
        self,
        modelname:str
    ):
        
        completion = self.client.chat.completions.create(
                model="YOUR-FINE-TUNED-MODEL-NAME",
                messages=[
                    {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
                    {"role": "user", "content": "Hello!"}
                ]
            )
    def fine_tune_model(self,file_path, model="gpt-3.5-turbo-1106"):
        try:
            # 创建文件
            file = self.client.files.create(
                file=open(file_path, "rb"),
                purpose="fine-tune"
            )

            # 启动微调任务
            fine_tuning_job = self.client.fine_tuning.jobs.create(
                training_file=file.id,
                model=model
            )
            job_id = fine_tuning_job.id

            # 轮询状态直到任务完成
            while True:
                job_status = self.client.fine_tuning.jobs.retrieve(job_id).status
                job_details = self.client.fine_tuning.jobs.retrieve(job_id)
                if job_status == "succeeded":
                    print("Successful!")
                    print(job_details)
                    break
                elif job_status == "failed":
                    print("Failed, please try again")
                    print(job_details.error)
                    break
                else:
                    print(f"State: {job_status}，wait")
                    time.sleep(10)  # 等待10秒后再查询任务状态

            # 如果任务成功，获取新模型的信息
            if job_status == "succeeded":
                new_model_id = job_details.fine_tuned_model
                organization_id = job_details.organization_id
                new_model_name = self.client.models.retrieve(new_model_id).name
                print(f"Name of new model: {new_model_name}。")

            return job_details

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def list_fine_tuning_jobs(self):
        try:
            # 获取所有微调作业
            jobs = self.client.fine_tuning.jobs.list()

            # 遍历作业并打印相关信息
            for job in jobs:
                fine_tuned_model_id = job.fine_tuned_model
                training_file_id = job.training_file
                training_file = self.client.files.retrieve(training_file_id)
                training_create_time = training_file.created_at
                training_create_time = datetime.datetime.fromtimestamp(training_create_time).strftime('%Y-%m-%d %H:%M:%S')
                training_file_json_name = training_file.filename

                print(f"Fine-tuned model name: {fine_tuned_model_id}, Training file: {training_file_json_name}, Training create time: {training_create_time}")

        except Exception as e:
            print(f"An error occurred: {e}")