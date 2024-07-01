# Bug Response
def bug_response():
    return ('For bug reports, please first review the [GitHub documentation](<https://github.com/jntm7/yumikord>).''\nIf it is unable to be resolved, feel free to [open a new issue](<https://github.com/jntm7/Yumikord/issues>).''\nPlease ensure the respective labels `enhancement` for feature requests and `bug` for issues are assigned.''\nFor feature requests and general inquiries, feel free to contribute to the [discussions page](https://github.com/jntm7/Yumikord/discussions).')

# No Message
def no_message_response():
    return 'Well, this is awkward...'

# Random Greeting
def choose_random_response(command):
    responses = {
        "greet": ["Hello!", "Hi!", "Hey!"],
        "bye": ["Goodbye!", "See you!", "Bye!"]
    }
    return responses.get(command, ["I don't understand."])[0]