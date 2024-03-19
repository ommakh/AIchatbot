import streamlit as st
import assemblyai as aai
from audio_recorder_streamlit import audio_recorder
import openai
import base64


def setup_openAI(api_key):
    return openai.OpenAI(api_key=api_key)

def transcribe_audio(client, audio_path):
    with open(audio_path,"rb") as audio_file:
        transcript = client.audio.transcriptions.create( model="whisper-1", file=audio_file)
        return transcript.text

def fetch_ai_response(client,input_text):
    message = [{"role":"user", "content":input_text}]
    response=client.chat.completions.create(model = "gpt-3.5-turbo-1106", messages=message)
    return response.choices[0].message.content

def text_to_audio(client, text, audio_path):
    response = client.audio.speech.create(model="tts-1", voice="alloy",input=text)
    response.stream_to_file(audio_path)


def auto_play_audio(audio_file):
    with open(audio_file,"rb") as audio_file:
        audio_bytes=audio_file.read()
    base64_audio=base64.b64encode(audio_bytes).decode("utf-8")
    audio_html=f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay>'
    st.markdown(audio_html, unsafe_allow_html=True)



def main():
    st.title("Leo chatbot")
    st.sidebar.title("API KEY CONFIGURATION")
    api_key  = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
     client = setup_openAI(api_key)
     recorded_audio=audio_recorder()
     if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file,"wb") as f:
            f.write(recorded_audio)
        transcribed_text=transcribe_audio(client, audio_file)
        st.write("transcribed text", transcribed_text)
        ai_response = fetch_ai_response(client, transcribed_text)
        response_audio_file = "audio_response.mp3"
        text_to_audio(client, ai_response, response_audio_file)
        st.audio(response_audio_file)
        st.write("Leo: ",ai_response)



    
if __name__=="__main__":
    main()




