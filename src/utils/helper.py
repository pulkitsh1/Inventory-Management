import os

ALLOWED_EXTENSIONS = ['png','jpeg','jpg','gif']
UPLOAD_FOLDER = os.getenv('upload_path', os.path.join( os.getcwd(), 'src', 'uploads', 'images'))
print("os.getcwd", os.getcwd())
print("upload folder ", UPLOAD_FOLDER)
def file_valid(file):
    return '.' in file and \
        file.rsplit('.',1),[1] in ALLOWED_EXTENSIONS