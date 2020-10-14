import re

def contains_failure(message):
    return "= FAILURES =" in message

def get_traceback(message):
    try:
        index = message.index("= FAILURES ")
    except ValueError:
        raise ValueError("Given message does not contain a traceback")

    for _ in range(3):
        index = message.index("\n", index + 1)

    end_index = message.rindex("short test summary info")
    end_index = message.rindex("\n", end_index)+1
    print(index, end_index)
    return message[index:end_index]


def get_summary(message):
    groups = re.search(r"=* short test summary info =*\nFAILED .*?::.*? - (.*)", message).groups()

    return groups[0]





