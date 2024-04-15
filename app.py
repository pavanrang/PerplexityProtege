# app.py
import streamlit as st
from search_engine import search_with_serper
from answer_generator import extract_citation_numbers, generate_answer, get_related_questions

def fetch_json_attributes(json_data, print=False):
    
    # Initialize empty lists for each key
    names = []
    urls = []
    snippets = []

    # Iterate over each item in the list and extract values for each key
    for item in json_data:
        names.append(item['name'])
        urls.append(item['url'])
        snippets.append(item['snippet'])

    if print:
        # Print the extracted values
        print("Names:", names)
        print("URLs:", urls)
        print("Snippets:", snippets)

    return names, urls, snippets

def main(query, contexts, urls):

    print("Sources ---->")
    for _url in urls:
        print(_url)

    print("\n\nAnswers --->")
    citations = extract_citation_numbers(generate_answer(query, contexts))
    print('\n'.join([f"Citation : {citation} --->  {urls[int(citation)-1]}" for citation in citations]))

                
    print("\n\nRelated Questions --->")
    get_related_questions(query, contexts)

def app():
    
    st.title("PerplexityProtege")
    query = st.text_input("Enter your question:")

    if query and st.button("Get Answer", use_container_width=True):
        contexts = search_with_serper(query)
        name, url, snippets = fetch_json_attributes(contexts)

        answer = generate_answer(query, contexts)
        st.subheader("Answer:")
        st.write(answer)

        st.subheader("Related Questions:")
        related_questions = get_related_questions(query, contexts)
        if related_questions:
            st.write(related_questions)
        else:
            st.write("No related questions found.")

        with st.expander("> Sources", expanded=False):
            for _url in url:
                st.write(_url)

if __name__ == "__main__":
    app()