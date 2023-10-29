import base64
import io
import os
import zipfile
import streamlit as st
from resume_matching import Resume_Matcher

default_jd = os.path.abspath("Java JD.docx")
default_resume = os.path.abspath("java-full-stack-developer-resume-example.pdf")
def calculate_score(uploadedResume, uploadedJd):
    obj = Resume_Matcher()
    resume_score = obj.match_resume(uploadedResume, uploadedJd)
    final_score = round(resume_score, 2)
    return final_score

def upload_default_file(default_file):
    with open(default_file, "rb") as file:
        local_file_contents = file.read()

    class CustomFile:
        def __init__(self, name, content):
            self.name = name
            self.content = content
            self.bytes_io = io.BytesIO(content)

        def read(self, size=-1):
            return self.bytes_io.read(size)

        def seek(self, position, whence=0):
            return self.bytes_io.seek(position, whence)

        def tell(self):
            return self.bytes_io.tell()

        def seekable(self):
            return self.bytes_io.seekable()

        def close(self):
            self.bytes_io.close()
    local_custom_file = CustomFile(default_file, local_file_contents)
    return local_custom_file

def resolve_files(uploadedJd, uploadedResume):
        if uploadedResume.name.split('.')[-1] == 'zip':
            results = {}
            with zipfile.ZipFile(uploadedResume, "r") as z:
                z.extractall('./extraced_resumes')
            print("zip extraced")
            for (root, dirs, files) in os.walk('.', topdown=True):
                print(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"file path is {file_path}")
                    if 'pdf' in file_path.split('.')[-1] or 'docx' in file_path.split('.')[-1]:
                        score = calculate_score(file_path, uploadedJd)
                        results[file] = score
                    else:
                        print(f"given format for file {file} is not supported")
                sort_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
                for result in sort_dict:
                    st.markdown(
                        f"Match percentage of resume **{result}** for **{uploadedJd.name}** is ***{sort_dict[result]}%***")

        else:
            score = calculate_score(uploadedResume, uploadedJd)
            st.markdown(
                f"Match percentage of resume **{uploadedResume.name}** for **{uploadedJd.name}** is ***{score}%***")


st.set_page_config(
    page_title= "AI Resume Matching",
    page_icon="📄",
    layout= "wide",
    initial_sidebar_state = "expanded"
)
st.markdown("<h1 style = 'text-align:center;'>AI Resume Matching</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    uploadedJd = st.file_uploader("Upload Job Description", type=['pdf', 'docx'])
with col2:
    uploadedResume = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'zip'])



col1, col2, col3 = st.columns(3)
with col2:
    button_style = '''<style> .stButton button{
                                background-color: orange ;
                                color: white ; 
                                float: center ;}
                       </style>         
                    '''
    if uploadedJd is not None and uploadedResume is not None:
        button_style = '''<style> .stButton button{
                                    background-color: green ;
                                    color: white ; 
                                    float: center ;}
                           </style>         
                        '''
    st.markdown(button_style, unsafe_allow_html=True)
    click = st.button("Calculate Score")


    if click :
        if uploadedJd is None:
            st.markdown("Please Upload Job Description")
        if uploadedResume is None :
            st.write("Please Upload resumes")
        if uploadedJd is not None and uploadedResume is not None:
            resolve_files(uploadedJd, uploadedResume)


cola, colb, colc, cold,cole, = st.columns(5)
with cole:
    button_style1 = '''<style> .button1{
                                    background-color: green ;
                                    color: white ;
                                    float: center ;}
                           </style>
                        '''

    st.markdown(button_style1, unsafe_allow_html=True)
    button1_style = "background-color: green; color: white; font-size: 18px;"
    use_default_files = st.button("Use Default Files and calculate score",key="button1", help="click me")
if use_default_files:
    file_data = b"Hello, this is some file content."
    uploadedJd = upload_default_file(default_jd)
    uploadedResume = upload_default_file(default_resume)
    download_jd = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64.b64encode(uploadedJd.read()).decode()}" download="Java Jd.docx">Default_Java_Jd</a>',
    download_resume = f'<a href="data:application/pdf;base64,{base64.b64encode(uploadedResume.read()).decode()}" download="java-full-stack-developer-resume-example.pdf">Default_Resume</a>',
    st.markdown(f"Default files are {download_jd} and {download_resume}", unsafe_allow_html=True)
    resolve_files(uploadedJd, uploadedResume)


