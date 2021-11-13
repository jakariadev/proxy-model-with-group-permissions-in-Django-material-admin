# accounts.utils.py
import time
import datetime
from django.contrib.contenttypes.models import ContentType

class FileUploadTo:
    '''
    FileUploadTo('folder_name', [plus_id=True, plus_date=False])
    To automate upload_to callable function for file uploading path
    '''

    def __init__(self, folder_name, plus_id=False, plus_date=False):
        self.folder_name = folder_name
        self.plus_id = plus_id
        self.plus_date = plus_date

    def __call__(self, instance, filename):
        ''' 
        CALL FileUploadTo
            [instance]: instance is an instance of a dango_model of an django_app
            [filename]: filename is the file name of a file comming from Field of django_model
        '''
        path = self.upload_location(instance, filename)
        # return 'documents/{}/{}.pdf'.format(instance.user.rfc, self.name)
        return path

    def upload_location(self, instance, filename):
        '''
        UPLOAD LOCATION
        It's generate path according to the given instance.
            PATH: <app_label>/<model>/<new_generated_filename>.<file_extension>
            Challenge: How can I get the field_name for which this function. In this case 'image' field name given by user. Then automate the upload_location function. [May be this is the solution]
                Solution: FileUploadTo('field_name')
        '''
        splitlist = filename.split(".")
        filebase, extension = splitlist[0], splitlist[-1]
        new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
        content_type = ContentType.objects.get_for_model(instance.__class__)
        app_label = content_type.app_label
        model_name = content_type.model
        folder_name = self.folder_name
        if self.plus_id and instance.id:
            folder_name = f'{folder_name}/{instance.id}'
        if self.plus_date:
            # "%Y/%m/%d/%H_%M_%S/"
            folder_name = f'{folder_name}/{datetime.date.today().strftime("%Y/%m/%d")}'
        return "%s/%s/%s/%s" % (app_label, model_name, folder_name, new_filename)

    # need to find out what is the purpose of
    #     ValueError: Cannot serialize: <accounts.utils.FileUploadTo object at 0x0000022264685C88>
    # There are some values Django cannot serialize into migration files.
    # For more, see https://docs.djangoproject.com/en/2.0/topics/migrations/#migration-serializing

    def deconstruct(self):
        return ('accounts.utils.FileUploadTo', [self.folder_name], {})
