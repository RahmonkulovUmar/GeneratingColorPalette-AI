import openai
import json
from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values("/etc/secrets/.env")
openai.api_key=config["OPENAI_API_KEY"] ###example .env file###  OPENAI_API_KEY=sk-RGYOvDBFqyNLekF4sdlSmImkju4jk7dhKJHIGH
 
app = Flask(__name__,
    template_folder='templates',
    static_url_path='',
    static_folder='static'
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.
    
    Q: Convert the following verbal description of a color palette into a list of colors: The Meadow
    A: ["#FFC300", "#FCCFA8", "#FFB84F", "#FF8E00", "#FF7B00", "#FB4707"]
    
    Q: Convert the following verbal description of a color palette into a list of colors: sage, native
    A: ["#FFDFC7", "#E48663", "#C9403A", "#A33232", "#775159", "#643D3D", "#302223"]
    
    Desired format: a JSON array of hexadecimal color codes
    
    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    
    example = openai.Completion.create(
        prompt= prompt,
        model="gpt-3.5-turbo-instruct",
        max_tokens=200,
    )

    colors = json.loads(example["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def promp_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

@app.route("/")
def index():
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Give me a funny word: "
    )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)