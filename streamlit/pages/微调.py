import streamlit as st
from utils.fine_utils import fine_utils_API
import os
from pathlib import Path
finetest = fine_utils_API()

def select_file_from_folder(
    folder_path:str, 
    file_types:list=None
    ):
    """
    在 Streamlit 应用中创建一个选择框，允许用户从指定文件夹中选择特定类型的文件。
    
    参数:
    - folder_path(str): 文件夹的路径
    - file_types(str): 可接受的文件类型集合，例如 {'.mp3', '.wav'}
    
    返回:
    - selected_file_path: 选中文件的完整路径，如果没有文件被选中则为 None
    """
    # 检查文件类型是否被指定，如果没有，则接受所有类型的文件
    if file_types is None:
        # 获取文件夹中所有文件
        audio_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    else:
        # 确保 file_types 是集合类型
        file_types_set = set(file_types)
        # 获取文件夹中所有符合类型的文件
        audio_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1] in file_types_set]
    
    # 如果文件夹中有文件，则显示一个选择框供用户选择
    if audio_files:
        
        audio_files.insert(0, None)
        selected_file = st.sidebar.selectbox('Select a file:', audio_files)
        
        # 获取选中文件的完整路径
        if selected_file:
            selected_file_path = os.path.join(folder_path, selected_file)
            return selected_file_path
    else:
        st.write("No files found with the given types in the folder.")
        return None


# 初始化会话状态
if 'stream_chat_history' not in st.session_state:
    st.session_state['stream_chat_history'] = []
    
    
# 显示聊天历史
def display_history():
    for message in st.session_state['stream_chat_history']:
        with st.chat_message(message["label"]):
            st.markdown(message["message"])
        
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = Path(ROOT_DIR) / "src" 
jsonpath = select_file_from_folder(folder_path =path )
input = st.chat_input("快输入点消息")

jobs_info = finetest.list_fine_tuning_jobs()
selectmodel = st.sidebar.selectbox("选择一个模型",jobs_info)

    
if st.button("微调启动"):
    finetest.fine_tune_model(file_path=jsonpath)

st.info(selectmodel)
if input and selectmodel is not None:
    # 将用户输入添加到历史记录中并显示
    st.session_state['stream_chat_history'].append({'label': 'user', 'message': input})
    
    Ai_res = finetest.chat_Models(modelname=selectmodel,systemset="你是og娘",input=input)
    st.session_state['stream_chat_history'].append({'label': 'AI', 'message': Ai_res})
    display_history()
    

