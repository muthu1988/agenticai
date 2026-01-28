from langchain_ollama import OllamaLLM
import json
import re # Added for cleaning markdown

# 1. Initialize local "Brain"
model = OllamaLLM(model="phi3.5")

def calculator(expression: str) -> str:
    """Useful for when you need to answer questions about math."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# 2. Test a simple prompt
def run_test(prompt):
    print("Agent is thinking...")
    
    response = model.invoke(f"""
        {prompt}
        
        RETURN: JSON this format ONLY: ```json
        {{
            "expression": "the mathematical expression generated",
            "llmanswer": "the calculated result only as number"
        }}
        ```
        NOTE: NO COMMENTS OR NOTE OR EXPLANATION
    """)

    print("AI Response:")
    print(response)

    try:
        # The re.DOTALL flag allows the dot (.) to match newlines
        match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)

        if match:
            # .group(1) extracts only the content inside the parentheses
            clean_response = match.group(1).strip()
        else:
            clean_response = response.strip()
        
        # PARSING: Convert string to dictionary
        data = json.loads(clean_response)

        print("\n API Data:")
        print(data)
        
        print("\nComputed answer:")
        # ACCESSING: Use data["expression"] instead of data.expression
        print(calculator(data["expression"]))
        
    except Exception as e:
        print(f"\nParsing Error: {e}")
        print("Raw output was not valid JSON.")
 
if __name__ == "__main__":
    run_test("what is 1234 times 5678")
