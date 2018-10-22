import os
import subprocess
import tarfile
import time
import urllib.request
from urllib.error import URLError

S3_IMAGES_PATH = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
LOCAL_STORAGE = '/public/images'
TMP_STORAGE = '/tmp/images.tar.gz'

HEALTH_TIMEOUT_SECS = 120
HEALTH_CHECK_DELAY_SECS = 1
HEALTH_CHECK_URL = 'http://127.0.0.1:3000/'


class Deployment(object):
    def __init__(self):
        self.deploy_success = False
        self.res = None
        self.check_local_path()
        self.set_working_directory()
        self.remove_running_deployment()

    @staticmethod
    def remove_running_deployment():
        if subprocess.check_output(['docker-compose', 'ps', '-q']):
            print('Stopping current deployment')
            subprocess.check_output(['docker-compose', 'down'])
            print('Current deployment stopped')

    @staticmethod
    def set_working_directory():
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def check_local_path():
        # check for extraction directories existence
        if not os.path.isdir(os.path.join(os.getcwd(), LOCAL_STORAGE)):
            os.makedirs(os.path.join(os.getcwd(), LOCAL_STORAGE))

    @staticmethod
    def download_files():
        print('Starting file download')
        filename, headers = urllib.request.urlretrieve(S3_IMAGES_PATH, TMP_STORAGE)
        print('Download completed')

    @staticmethod
    def setup_images_locally():
        try:
            print('Extracting files...')
            tar = tarfile.open(TMP_STORAGE, "r:gz")
            tar.extractall(LOCAL_STORAGE)
            tar.close()
            print('Files extraction successful [{}]'.format(LOCAL_STORAGE))
        except Exception as e:
            print('Extraction failed due to error [{}] - Failing deployment!'.format(e))
            exit(1)

    def run_docker_compose_deploy(self):
        self.deploy_success = not subprocess.check_output(['docker-compose', 'up', '-d'])
        print(self.deploy_success)

    def app_health(self):
        try:
            r = urllib.request.urlopen(HEALTH_CHECK_URL, timeout=1)
            d.res = r and r.getcode()
            return d.res
        except:
            return

    def print_status(self, t):
        print('\rRunning health check{}'.format('.' * int((t % 4))), end="")


if __name__ == "__main__":
    print('Start new deployment')
    d = Deployment()
    d.download_files()
    d.setup_images_locally()
    d.run_docker_compose_deploy()

    if d.deploy_success:
        timeout = 0
        while d.app_health() != 200 and timeout <= HEALTH_TIMEOUT_SECS:
            d.print_status(timeout)
            time.sleep(HEALTH_CHECK_DELAY_SECS)
            timeout += HEALTH_CHECK_DELAY_SECS

        print('\n')
        if d.res == 200:
            print('Deployment completed - Health status ({})'.format(d.res))
            exit(0)
        elif d.res == 500:
            print('Deployment failed - Health status ({})'.format(d.res))
            exit(1)
        else:
            print('Deployment timeout out [{}]'.format(timeout))
            exit(1)
    else:
        print('Deployment failure')
        exit(1)
