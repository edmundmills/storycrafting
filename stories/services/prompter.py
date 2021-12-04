import openai

class Prompter:
    @staticmethod
    def prompt(params):
        response = openai.Completion.create(**params)
        text = response['choices'][0]['text']
        return text

    @staticmethod
    def generate_proposal_prompt(proposal):
        thoughts = proposal.thoughts.all()
        facts = proposal.facts.all()
        story_title = proposal.step.story.title
        story_text = proposal.step.prompt
        prompt = ""
        if len(thoughts) == 0 and len(facts) == 0 and not story_text:
            prompt += f"Write a story below.\n"
            prompt += f"{story_title}, a story."
        elif len(thoughts) + len(facts) > 0:
            prompt = "Write a story with the following elements:\n"
            prompt += f"- The story is titled {story_title}\n"
            prompt += "".join(f"- {fact}\n" for fact in proposal.facts.all())
            prompt += "".join(f"- {thought}\n" for thought in proposal.thoughts.all())
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
        return params      

    @staticmethod
    def update_context_prompt(step):
        initial_facts = step.previous_proposal.facts.all()
        story = step.prompt
        prompt = ""
        if len(initial_facts) > 0:
            prompt += story + "\n"
            prompt += "\n"
            prompt += 'Based on the paragraph above, which of the following facts about the situation have changed?\n'
            prompt += "".join(f"- {fact}\n" for fact in initial_facts)
            prompt += "\n"
            prompt += "Updated facts about the situation:\n"
        else:
            prompt += 'Write a list of facts from the following paragraph that are important for the story:\n'
            prompt += story + "\n"
            prompt += "\n"
            prompt += "Key facts:\n"

        prompt += "-"
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
        return params
            




