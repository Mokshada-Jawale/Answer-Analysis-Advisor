import streamlit as st
from groq import Groq


def generate_response(input_dict, custom_instruction):
    # Update the API key with your valid API key
    groq_api = "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"
    client = Groq(api_key=groq_api)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": custom_instruction},
            {"role": "user", "content": f"Analyze the provided answer and give advise on that {input_dict}"},
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=500,
        top_p=1,
    )

    llm_output = chat_completion.choices[0].message.content
    llm_output = llm_output.replace("**", "")
    llm_output = llm_output.replace("*", "")
    return llm_output


def process_data(data, custom_instruction):
    response = {}
    for data_dict in data:
        response_text = generate_response(data_dict, custom_instruction)
        response[data_dict['question']] = response_text
    return response


# Custom instruction
custom_instruction = """
You will receive an input context in the form of a dictionary containing 'question' and 'answer' keys, both related to software engineering. Perform the following steps:

1. Read the question and the corresponding answer carefully.
2. Determine what an ideal answer to the question should include. Compare the student's answer to this ideal response.
3. Analyze how well the student's answer addresses the question and provide analysis on the student's understanding of the topic.
4. Give specific information about, what is correct in the student's answer, what is incorrect, and how the answer can be improved for better accuracy.
5. Mention whether the student's answer shows a poor or good understanding of the topic and specify which aspects demonstrate this understanding.
6. Suggest study material links from GeeksforGeeks, Tutorialspoint, or Javatpoint that the student should refer to for a better understanding of the topic, ensuring that the study material link is valid.
7. If the answer does not address the question, mention what the student's answer is related to and explain what should be included in the answer to correctly address the question.
8. Give advise to students in clear and easy-to-understand language, avoiding AI-generated jargon.
9. Give specific details rather than general statements and avoid mentioning repeating points. Write advise in just 5-6 lines.
10. If the question and answer are not related to software engineering, respond with "Please provide material regarding software engineering subject."
11. You can refer to this format:

    Your answer gives [basic/poor/good] understanding of [topic], you correctly mentioned these [points], but needs precise definitions and details. Clarify that [provide detailed explanation]. Mention steps like [list steps if applicable]. For [related topic], explain that it involves [detailed explanation]. Also mention [additional relevant information]. Mention benefits like [list benefits] to enhance your response. For improvement, read your class notes and refer to these articles: [provide links to study materials].

Input context: {input_dict}
"""

# Streamlit Interface
st.title("Answer Analysis Advisor")

# Input section
st.header("Input the Question and Answer")
question = st.text_input("Question", "Enter your question here")
answer = st.text_area("Answer", "Enter your answer here")

if st.button("Analyze the answer"):
    data = [{'question': question, 'answer': answer}]
    feedback_dict = process_data(data, custom_instruction)
    for question, feedback_text in feedback_dict.items():
        st.subheader("Question and Answer")
        st.write(f"**Question**: {question}")
        st.write(f"**Answer**: {answer}")
        st.subheader("Response")
        st.write(feedback_text)
