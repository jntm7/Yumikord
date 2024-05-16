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
        return f'You rolled: {roll_dice()}'
    elif 'flip a coin' in lowered:
        return f'You got: {flip_coin(user_input)}'
    else:
        return choose_random_response(lowered)  
        
        choice(['I do not quite understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])

def roll_dice() -> int:
    return random.randint(1,6)

def flip_coin() -> str:
    result = random.choice(['heads', 'tails'])

def choose_random_response(user_input: str) -> str:
    responses: Final[str] = [
        'I do not quite understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?
    ]
    return random.choice(responses) if user_input else 'You didn't say anything'
