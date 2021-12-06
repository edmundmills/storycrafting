import openai

def trim_incomplete_sentences(text):
    return '.'.join(text.split('.')[:-1]) + '.'

def trim_whitespace(text):
    return text.strip()

def insert_bullets(text):
    if not text:
        return text
    return ''.join(f"- {line}\n"for line in text.split('\n')) 

class Prompter:    
    @staticmethod
    def prompt(params):
        response = openai.Completion.create(**params)
        text = response['choices'][0]['text']
        return text

    @staticmethod
    def generate_proposal(proposal):
        story_title = proposal.step.story.title
        story_text = proposal.step.prompt
        context_text = insert_bullets(proposal.context_text)
        reasoning_text = insert_bullets(proposal.reasoning_text)
        prompt = ""
        if not context_text and not reasoning_text and not story_text:
            prompt += f"Write a story below.\n"
            prompt += f"{story_title}, a story."
        elif context_text or reasoning_text:
            prompt = "Write a story with the following elements:\n"
            prompt += f"- The story is titled {story_title}\n"
            prompt += context_text
            prompt += reasoning_text
        prompt += story_text or 'Response:'
        print(prompt)
        params = {
            'prompt': prompt,
            'engine': 'davinci',
            'temperature': 0.5,
            'max_tokens': 150,
            'frequency_penalty': 1.25,
            'top_p': 1,
            'presence_penalty': 0,
            'logprobs': None,
        }
        response = "\t  test. sdfg" # Prompter.prompt(params)
        response = trim_incomplete_sentences(response)
        response = trim_whitespace(response)
        return response

    @staticmethod
    def updated_context(step):
        initial_context_text = insert_bullets(step.previous_proposal.context_text)
        story = step.prompt
        prompt = ""
        if initial_context_text:
            prompt += story + "\n"
            prompt += "\n"
            prompt += 'Based on the paragraph above, how have the following facts about the situation have changed?\n'
            prompt += initial_context_text
            prompt += "Updated facts about the situation:\n"
        else:
            prompt += 'Write a list of facts from the following paragraph that are important for the story:\n'
            prompt += story + "\n"
            prompt += "\n"
            prompt += "Key facts:\n"

        prompt += "-"
        print(prompt)
        params = {
            'prompt': prompt,
            'engine': 'davinci-instruct-beta-v3',
            'temperature': 0.5,
            'max_tokens': 100,
            'frequency_penalty': 0.25,
            'top_p': 1,
            'presence_penalty': 0,
            'logprobs': None,
        }
        response = 'test' #Prompter.prompt(params)
        return response
            




