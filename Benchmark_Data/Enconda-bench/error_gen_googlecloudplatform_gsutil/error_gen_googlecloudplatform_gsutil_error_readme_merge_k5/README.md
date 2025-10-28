# gsutil

gsutil is a Python application that lets you access Google Cloud Storage from
the command line. You can use gsutil to do a wide range of bucket and object
management tasks, including:

* Creating and deleting buckets. For example, to create a bucket, use `gsutil create bucket <bucket_name>`.



* Uploading, downloading, and deleting objects.
* Listing buckets and objects.
* Moving, copying, and renaming objects.
* Editing object and bucket ACLs.

## Installation

Please ensure you have the `boto3` Python library installed, as it is a core dependency for gsutil.




For installation instructions, please see:

https://cloud.google.com/storage/docs/gsutil_install

You will also need to install the required system dependencies by running `sudo apt-get install libxml2-dev libxslt1-dev python3-dev` and then `pip install -r dependencies.txt`.


## Testing / Development

The gsutil source code is available at https://github.com/GoogleCloudPlatform/gsutil

To set up a development environment, first install all dependencies by running `pip install -r requirements.txt` from the root of the repository. Then, create and activate a Python virtual environment.





See https://cloud.google.com/storage/docs/gsutil/addlhelp/ContributingCodetogsutil
for best practices on how to contribute code changes to the gsutil repository.

## Help and Support

Run the "gsutil help" command for a list of the built-in gsutil help topics.





You can also browse the help pages online at:

https://cloud.google.com/storage/docs/gsutil

For community support, visit:

https://cloud.google.com/storage/docs/resources-support#community
