from main import *
from grades_homework import *


def check_for_mention(split_by_word, target, index):
    """
    Performs a simple check to see if there is a word which matches the requirements for a discord mention: starting with <@ and ending in >.
    """
    if split_by_word[index].startswith("<@") and split_by_word[index].endswith(">"):
        target = (split_by_word[index])
        return target
    else:
        return None
    

def check_for_karma(split_by_word, index):
    """
    Checks if there is a word that only contains + or - symbols. Return the karma sum if so. If not, return None
    """
    if all(character == "+" or character == "-" for character in split_by_word[index]):
        karma = count_karma(split_by_word[index])
        return karma
    else:
        return None


def count_karma(content):
    """
    A simple function that determines the sum of + and - in a word. Returns the sum.
    """
    karma_total = content.count("+") - content.count("-")
    return karma_total


def determine_user_karma(number_of_mentions, karmajson, target, karma_dict, karma_total, karma_to_print):
    """
    Loads the existing karma for each user and updates each of them with the new karma.
    """
    x = 0
    for n in range(number_of_mentions):
        existing_karma = 0
        stored_karma = initialise_and_load(karmajson)
        existing_karma = stored_karma.get(f"{list(target)[x]}")
        try:
            int(existing_karma)
        except:
            existing_karma = 0
        update_karma = karma_total + existing_karma
        karma_dict.update({f"{list(target)[x]}": update_karma})
        karma_to_print += f"{list(target)[x]}: {karma_dict[list(target)[x]]}\n"
        new_karma = karma_dict
        stored_karma.update(new_karma)
        sorted_karma = dict(sorted(stored_karma.items(), key = lambda item: item[1], reverse = True))
        write_file(sorted_karma, karmajson)
        x = x + 1
    return karma_to_print


def show_karma(existing_karma):
    """
    Loads the stored karma and sends a message with all the karma together
    """
    i = 0
    karma = ""
    for n in existing_karma:
        karma_user = list(existing_karma)[i]
        if existing_karma[f"{karma_user}"] != 0:
            karma+=(f"{karma_user}: {existing_karma[f"{karma_user}"]}\n")
        i = i + 1
    return karma