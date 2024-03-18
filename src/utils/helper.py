ALLOWED_EXTENSIONS = ['png','jpeg','jpg','gif']
UPLOAD_FOLDER = 'src/uploads/images/'

def file_valid(file):
    return '.' in file and \
        file.rsplit('.',1),[1] in ALLOWED_EXTENSIONS