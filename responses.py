from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, this is awkward...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Great, thanks!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1,6)}'
    elif 'flip a coin' in lowered:
        result = random.choice(['heads', 'tails'])
        await message.author.send(f'You got: {result}')
    else:
        return choice(['I do not quite understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])
