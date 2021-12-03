import openai

class Prompter:
    @classmethod
    def prompt(cls, prompt, engine='davinci', temperature=0.3,
               max_tokens=150, frequency_penalty=1.25):
        response = openai.Completion.create(
            engine=engine,
            prompt = prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=frequency_penalty,
            presence_penalty=0,
            logprobs=None,
            )
        text = response['choices'][0]['text']
        text = '.'.join(text.split('.')[:-1]) + '.'
        return text
