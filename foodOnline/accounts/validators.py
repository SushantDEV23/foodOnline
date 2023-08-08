from django.core.exceptions import ValidationError
import os

def allow_only_iamge_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.png', '.jpeg', '.jpg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported format. Allowed extensions : ' + str(valid_extensions))