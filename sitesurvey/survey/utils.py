import secrets
import os

from sitesurvey import app

def save_file(form_file, folder_name):
    """
    Generates random hex value (to prevent file name collisions) as file name and
    saves the file to servers file system.
    Returns the generated filename so it can be stored in DB and linked to surveys
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_file.filename)
    file_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path,'static/', folder_name, file_filename)
    form_file.save(picture_path)
    return file_filename
