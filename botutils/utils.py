def get_reply_message_for_fic_blacklist(data):
    """to return a simple reply message when fic blacklist cog is used"""
    if data["resp"] == "404_WRONG_URL":
        return "Can't add fic to blacklist. Not a valid url or index."
    elif data["resp"] == "200_VOTE_ADDED":
        return "Your vote was added."
    elif data["resp"] == "200_STORY_AND_VOTE_ADDED":
        return "New story added to blacklist."
    else:
        print("Server error.", data)
        return None