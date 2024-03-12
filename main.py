from fastapi import FastAPI
from langchain_community.llms.ollama import Ollama
import uvicorn
import os
import random
import string

app = FastAPI()

def extract_between(text):
    """
    Extracts the string between the first occurrence of ` and ` in the text.

    Args:
        text: The string to extract from.

    Returns:
        The string between ` and `, or None if not found.
    """
    start = text.find("```")
    if start == -1:
        return None  # Not found
    end = text.find("```", start + 3)  # Search after starting delimiter
    if end == -1:
        return None  # Closing delimiter not found
    return text[start + 3:end]  # Extract substring between delimiters


@app.get("/")
async def root():
    """
    A function that handles requests to the root endpoint. It returns a dictionary with a message property.
    """

    return {"message": "Hello World"}

@app.get("/api/code")
async def code(prompt):
    """
    A function that handles requests to the '/api/code' endpoint. It takes a prompt as a parameter and uses the Ollama model to invoke the prompt and return the result.
    """
    llm = Ollama(model="llama2")
    res = llm.invoke(prompt)
    extracted_code = extract_between(res)
    if extracted_code is not None:
        # Remove newlines from the code string
        code_without_newlines = extracted_code.replace("\n", "")
        # Generate a human-readable filename
        filename_base = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        filename = f"{filename_base}.py"

        # Ensure filename uniqueness (optional)
        while os.path.exists(filename):
            filename_base = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            filename = f"{filename_base}.py"

        # Write the code to the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(code_without_newlines)

        # Return a JSON object indicating success and the filename
        return {"message": "Code saved to file", "filename": filename}
    
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

