import gradio as gr
from gtts import gTTS
import tempfile
import os

def generate_speech(text, language):
    if not text.strip():
        return None, "Please enter some text!"
    
    try:
        lang_map = {
            'English': 'en', 'Hindi': 'hi', 'Spanish': 'es', 
            'French': 'fr', 'German': 'de', 'Italian': 'it',
            'Japanese': 'ja', 'Korean': 'ko', 'Chinese': 'zh'
        }
        
        lang_code = lang_map.get(language, 'en')
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tts.save(f.name)
            return f.name, f"✅ Audio generated in {language}!"
            
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft(), title="TTS Voice Studio") as demo:
    gr.Markdown("""
    # 🎤 Text-to-Speech Studio
    *Convert text to speech in multiple languages*
    """)
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Enter your text",
                placeholder="Type what you want to convert to speech...",
                lines=4
            )
            
            language = gr.Dropdown(
                choices=['English', 'Hindi', 'Spanish', 'French', 'German', 
                        'Italian', 'Japanese', 'Korean', 'Chinese'],
                value="English",
                label="Language"
            )
            
            generate_btn = gr.Button("Generate Speech", variant="primary")
        
        with gr.Column():
            audio_output = gr.Audio(label="Generated Speech", type="filepath")
            status = gr.Textbox(label="Status", interactive=False)
    
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, language],
        outputs=[audio_output, status]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )