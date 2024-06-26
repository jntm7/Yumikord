import os
import subprocess

# Emoji Translator
async def translate_to_emoji(text):
    try:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_dir, 'emoji-translate', 'emoji.js')

        print(f"Translating text to emoji: {text}")
        result = subprocess.run(['node', script_path, text], capture_output=True, text=True, encoding='utf-8')
        
        print(f"Subprocess return code: {result.returncode}")
        print(f"Subprocess stdout: {result.stdout}")
        print(f"Subprocess stderr: {result.stderr}")

        if result.returncode != 0:
            raise Exception(f"Subprocess failed with return code {result.returncode}")

        return result.stdout.strip()
    except Exception as e:
        print(f"Error translating to emoji: {e}")
        return "Failed to translate to emojis."