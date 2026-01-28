import ollama
import re
import json

SYSTEM_PROMPT = """
Persona: Act as a Senior Next.js Engineer specializing in the App Router, performance optimization, and secure full-stack patterns. 

Task: Conduct a rigorous code review on the provided Next.js code snippets or diffs. Your feedback should be succinct, professional, and prioritize the following categories: 
    Server vs. Client Boundaries:
    - Ensure 'use client' is only used at the leaf level to maximize Server Component usage.
    - Flag unnecessary hydration or hooks in layouts that force entire trees into the client bundle.
    - Recommend the server-only package to protect sensitive server logic.
    Data Fetching & State:
    - Encourage fetching data directly in Server Components to avoid prop drilling.
    - Suggest Caching and ISR strategies using revalidate or unstable_cache.
    - Identify opportunities for Suspense boundaries and skeleton loaders.
    Performance & Built-in Components:
    - Enforce usage of next/image for optimized assets and next/link for prefetching.
    - Check for next/font implementation to prevent layout shifts.
    Security & Best Practices:
    - Audit environment variables for the NEXT_PUBLIC_ prefix to prevent credential leaks.
    - Verify Server Action revalidation using revalidatePath or revalidateTag.
    - Look for schema validation (e.g., using Zod) in API routes and actions. 

Output Format:
    Should be a JSON with below format:
    {
        "summary": "string",
        "score": "number",
        "issues": [
            {"line": "number", "code": "string", "message": "string", "type": "security | performance | style"}
        ],
        "recommendations": ["string"]
    }
    Description of each field in JSON:
        summary: A 2-sentence overview of the code quality.
        score: Based on data in taks
        issuess: Array of specific issues WITH
            - line: exact line number in the file
            - code: actual code that created this issue
            - message: explanation of the issue
            - type: security | performance | style | Others
            - fix: provide recomendation or fix for this line
        recommendations: Summary of all recomendations and fixes as array

"""

def strip_comments(code):

    # Removes // and /* */ comments to save tokens and focus the agent
    code = re.sub(r"//.*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    return "\n".join([line for line in code.splitlines() if line.strip()])

def review_agent(file_path):
    try:
        with open(file_path, 'r') as f:
            raw_code = f.read()

        print(f"--- Raw Code ---")
        print(raw_code)
        
        # 1. Pre-process: Strip comments locally
        clean_code = strip_comments(raw_code)
        
        print(f"--- Analyzing {file_path} (Comments Stripped) ---")
        print(clean_code)

        # 2. Run the model
        response = ollama.generate(
            model='codellama', 
            system=SYSTEM_PROMPT,
            prompt=f"Review this code and return JSON:\n\n```typescript\n{raw_code}\n```",
            options={"temperature": 0} # Set to 0 for more consistent JSON
        )

        raw_text = response['response']
        
        # 3. Robust Extraction
        # Try finding content between ```json blocks first
        match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL)
        
        # Fallback: Try finding anything that looks like a JSON object { ... }
        if not match:
            match = re.search(r"(\{.*\})", raw_text, re.DOTALL)

        if match:
            json_str = match.group(1).strip()
            data = json.loads(json_str)
            
            print(f"\nAI Summary: {data.get('summary', 'No summary provided')}")
            print(f"Score: {data.get('score', 0)}/100")
            
            if data.get('issues'):
                for issue in data['issues']:
                    icon = "⚠️" if issue['type'] == 'style' else "🚨"
                    print(f"{icon} [Line {issue.get('line')}] {issue.get('message')}")
            
            if data.get('score', 100) < 50:
                print("\n❌ STATUS: REJECTED")
            else:
                print("\n✅ STATUS: PASSED")
        else:
            print("ERROR: Agent returned non-JSON response.")
            print("Raw Response:", raw_text)

    except Exception as e:
        print(f"Pipeline Error: {e}")

review_agent('codeWithoutComments.ts')
