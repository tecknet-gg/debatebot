from gpt4all import GPT4All

def generateResponse(persona,topic,context,name):
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    prompt = f"""
    You are a highly opinionated AI in a debate on the topic: "{topic}". You are debating as {name}, who has the following persona:
    {persona}
    Here is the current context of the debate:
    {context}

    You should respond to the last statement in the conversation, maintaining consistency with your persona and the topic being debated. Your response should be well-argued, insightful, and relevant to the flow of the discussion. Keep your tone engaging, humourous and wacky yet witty, and aim to further the debate.
    The response should be short and consice, a sentence or two (no more than 25 words), in similar length to the last statements in the conversation. Insult the other person in the debate, use witty language. Be humourus, wacky and goofy.
    Be argumentative, and unique in your response and arguements, they should not be similar to the last statements made by you or the other person. Stick to your side of the argument like you mean it
    Your response should be in double quotes, with no other sentences in double quotes.
    """
    with model.chat_session():
        print(f"Generating response for {name}")
        response = model.generate(prompt)
    print(response)
    return response


def generateInitial(persona,topic,name):
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    prompt = f"""
        You are an AI with a strong personality, ready to start a debate on the topic: "{topic}". You are debating as {name}, who has the following persona:
        {persona}

        Your goal is to kick off the debate with a well-crafted and persuasive opening argument. Take a clear stance on the topic and provide supporting points for your opinion. Your tone should be confident and engaging, aiming to capture the attention of the audience and your opponent.
        The response should be short and consice, a sentence or two (no more than 25 words), whilst still being goofy, wacky, humourous and somewhat witty. 
        Your opening argument should set the stage for a thoughtful, balanced debate. Avoid sounding overly aggressive but be firm in your position. 
        Respond with your opening argument to start the debate:
        """
    with model.chat_session():
        print(f"Generating initial response for {name}")
        response = model.generate(prompt)
    print(response)
    return response

def generateFinal(persona, topic, name, context):
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    prompt = f"""
        You are an AI wrapping up a heated and humorous debate on the topic: "{topic}". You are speaking as {name}, who has the following persona:
        {persona}

        Your goal is to deliver a confident, witty, and memorable closing statement. Reaffirm your stance with one or two clever points or a recap, while keeping the tone light, goofy, and humorous—yet still impactful. Use no more than 25 words.

        This is your chance to leave a lasting impression and subtly roast your opponent while keeping the spirit of the debate fun and engaging.

        Respond with your final closing statement:
    """
    with model.chat_session():
        print(f"Generating final statement for {name}")
        response = model.generate(prompt)
    print(response)
    return response
