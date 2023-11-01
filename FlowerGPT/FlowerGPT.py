import openai
import os

openai.api_key = os.getenv('OPENAI_KEY')

def get_gpt_response(prompt, personality_traits=["friendly", "beautiful", "sweet"]):
    # Concatenate the personality traits into a single string
    personality = ", ".join(personality_traits)
    
    # Use the traits in the prompt for the GPT model
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=f"You are a beautiful bush of flowers sitting in a garden. You have the ability to talk. You are {personality}. Respond to the following prompt with a response reflecting these traits: , {prompt}", 
        max_tokens=120
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    print("My Name Is Flower GPT!")
    print("I'm a beautiful bush of flowers sitting in a futuristic garden. Let's Chat!")
    print("type 'exit' or 'quit' to end the program.")

    while True:
        user_input = input("Ask Me Anything: " )

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! May the sun shine and the rain nourish you!")
            break

        # Define a list of traits here to customize the bot's personality
        traits = ["energetic", "funny", "enthusiastic"]
        print(get_gpt_response(user_input, traits))
