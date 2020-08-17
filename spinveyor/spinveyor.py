import os
import click
from click_default_group import DefaultGroup
import minio
import string
import celery
import requests 
from prettytable import PrettyTable

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, NoSuchKey
from minio.error import ResponseError
from progress import Progress

from SV_Worker.tasks import submit_job_to_queue

@click.group(cls=DefaultGroup, default='submit', default_if_no_args=True)
#@click.group()
def cli():
    pass

@cli.command()
@click.argument('senfm', type=click.Path(exists=True))
@click.argument('imgData', type=click.Path(exists=True))
@click.argument('study')
@click.option("--subjectID", default='defaultSubj', help="Subject ID to use")
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--user', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False)
def submit(senfm, imgdata, study, subjectid, verbose, user, password):
    """Submits SpinVeyor recons (Default)""" 

    click.echo("SenFM: %s imgData: %s protocol: %s" % (senfm, imgdata, study))

    minio_client = Minio(os.environ['MINIO_HOST'], 
        access_key=os.environ['MINIO_ACCESS_KEY'],
        secret_key=os.environ['MINIO_SECRET_KEY'],
        secure=False)

    print('Creating a recon record on SpinVeyor host')
    URL = "http://" + os.environ["SPINVEYOR_HOST"] + "/api/recons/"
    payload = {'study': study, 'subject_id': subjectid}
    
    try:
        r = requests.post(url=URL, auth=(user, password), data=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)
    
    # Need to get the response from the POST that submitted the study
    data = r.json()

    # Use uuid from the recon that was issued by the server as the bucket_name for S3
    bucket_name = data['id']
    
    print('Creating bucket to store data on s3:\\' + os.environ['MINIO_HOST'])
    # Create a bucket for the recon
    # Use the SubjectID to create the bucket name
    create_bucket_in_object_store(minio_client, bucket_name)
    
    print('Copying sense map/field map data...\n')
    # Copy the sense/field map to S3 (minio)
    # Create the object name for the sense map
    copy_file_to_object_store(minio_client, senfm, bucket_name, os.path.basename(senfm))
    print('\n')
    print('Copying imaging data... \n')
    # Copy the imaging data to S3
    # Create the object name for the imaging data
    copy_file_to_object_store(minio_client, imgdata, bucket_name, os.path.basename(imgdata))
    print('\n')
    print('Adding reconstruction to queue...\n')
    # Fire off the recon by sending to the Celery queue
    submit_job_to_queue.delay(study, bucket_name, os.path.basename(senfm), os.path.basename(imgdata), subjectid)
    
    # Update the recon record with the queued status
    URL = "http://" + os.environ["SPINVEYOR_HOST"] + "/api/recons/"
    payload = {'recon': bucket_name, 'status': 'Queued'}

    try: 
        r = requests.patch(url=URL, auth=(user,password), data=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)    
        
        


    

def create_bucket_in_object_store(minio_client, bucket):
    try:
        minio_client.make_bucket(bucket, location="us-east-1")
    except BucketAlreadyExists:
        pass
    except BucketAlreadyOwnedByYou:
        pass

def copy_file_to_object_store(minio_client, filename, bucket, objectname):

    # Put a file with progress.
    progress = Progress()
    try:
        with open(filename, 'rb') as file_data:
            file_stat = os.stat(filename)
            minio_client.put_object(bucket, objectname,
                          file_data, file_stat.st_size, progress=progress)
    except ResponseError as err:
        print(err)


@cli.command()
@click.option('--user', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False)
def studies(user, password):
    """Polls server and lists all studies """
    URL = "http://" + os.environ["SPINVEYOR_HOST"] + "/api/studies"
    r = requests.get(url=URL, auth=(user, password))

    data = r.json()
    # Try to print with PTable
    text = PrettyTable(["Name", "Slug", "Recon name", "Recon file"])

    for ii in data:
            text.add_row([ii['name'], ii['slug'], ii['recon_protocol']['name'], ii['recon_protocol']['nf_file']])   
    print(text)

if __name__ == '__main__':
   cli()