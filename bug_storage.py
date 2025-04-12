
bug_list = []

def add_bug(title, description, log_text, screenshot_path=None):
    bug = {
        "title": title,
        "description": description,
        "log": log_text,
        "screenshot": screenshot_path
    }
    bug_list.append(bug)

def get_all_bugs():
    return bug_list
