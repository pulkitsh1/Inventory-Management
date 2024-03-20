import os

ALLOWED_EXTENSIONS = ['png','jpeg','jpg','gif']
UPLOAD_FOLDER = os.getenv('upload_path', os.path.join(os.sep, os.getcwd(), 'src', 'uploads', 'images'))
def file_valid(file):
    return '.' in file and \
        file.rsplit('.',1),[1] in ALLOWED_EXTENSIONS