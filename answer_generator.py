# answer_generator.py
import re
from openai import OpenAI
from config import GROQ_API

_rag_query_text = """
You are a large language AI assistant built by pavan. You are given a user question, and please write clean, concise and accurate answer to the question. You will be given a set of related contexts to the question, each starting with a reference number like [[citation:x]], where x is a number. Please use the context and cite the context at the end of each sentence if applicable.

Your answer must be correct, accurate and written by an expert using an unbiased and professional tone. Please limit to 1024 tokens. Do not give any information that is not related to the question, and do not repeat. Say "information is missing on" followed by the related topic, if the given context do not provide sufficient information.

Please cite the contexts with the reference numbers, in the format [citation:x]. If a sentence comes from multiple contexts, please list all applicable citations, like [citation:3][citation:5]. Other than code and specific names and citations, your answer must be written in the same language as the question. If there are too many citations, choose the best of them
Here are the set of contexts:

{context}

Remember, don't blindly repeat the contexts. And here is the user question:
"""

_more_questions_prompt = """
You are a helpful assistant that helps the user to ask related questions, based on user's original question and the related contexts. Please identify worthwhile topics that can be follow-ups, and write questions no longer than 20 words each. Please make sure that specifics, like events, names, locations, are included in follow up questions so they can be asked standalone. For example, if the original question asks about "the Manhattan project", in the follow up question, do not just say "the project", but use the full name "the Manhattan project". The format of giving the responses and generating the questions shoudld be like this:

1. [Question 1]
2. [Question 2] 
3. [Question 3]

Here are the contexts of the question:

{context}

Remember, based on the original question and related contexts, suggest three such further questions. Do NOT repeat the original question. Each related question should be no longer than 20 words. Here is the original question:
"""

def extract_citation_numbers(sentence):
    # Define a regular expression pattern to match citation numbers
    pattern = r'\[citation:(\d+)\]'

    # Use re.findall() to extract all citation numbers from the sentence
    citation_numbers = re.findall(pattern, sentence)

    # Return the extracted citation numbers as a list
    return citation_numbers

class AI():
    def Groq(system_prompt, query):

        client = OpenAI(
            base_url = "https://api.groq.com/openai/v1",
            api_key=GROQ_API
            )
        llm_response = client.chat.completions.create(
            model="llama2-70b-4096",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Initialize an empty list to accumulate chunks
        chunks = []
        
        # Print real-time response and accumulate chunks
        for chunk in llm_response:
                
            try:
                if chunk.choices[0].delta.content is not None:
                    # Print real-time response
                    print(chunk.choices[0].delta.content, end="")
                    # Accumulate chunk
                    chunks.append(chunk.choices[0].delta.content)
            except:
                pass


        print("\n\n")
        # Join chunks together to form the complete response
        complete_response = ''.join(chunks)

        return complete_response
    
def get_related_questions(query, contexts):
        
        system_prompt = _more_questions_prompt.format(
                            context="\n\n".join([c["snippet"] for c in contexts])
                        )

        try:
            complete_response = AI.Groq(system_prompt, query)
            return complete_response
        
        except Exception as e:
            print(e)
            # For any exceptions, we will just return an empty list.
            return []
        
def generate_answer(query, contexts):

    # Basic attack protection: remove "[INST]" or "[/INST]" from the query
    query = re.sub(r"\[/?INST\]", "", query)

    system_prompt = _rag_query_text.format(
                context="\n\n".join(
                    [f"[[citation:{i+1}]] {c['snippet']}" for i, c in enumerate(contexts)]
                )
            )

    try:
        complete_response = AI.Groq(system_prompt, query)
        return complete_response

    except Exception as e:
        print(e)
        return "Failed Response"