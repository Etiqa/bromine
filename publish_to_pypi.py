# pylint: disable=invalid-name


import sys
assert sys.version_info.major >= 3, 'This script requires Python 3.'
del sys


import argparse
import hashlib
import io
from pathlib import Path, PurePath
import re
import subprocess
import tempfile

import requests
from six.moves.urllib.parse import urlsplit, urlunsplit, urljoin


# get version (= git tag) to publish
parser = argparse.ArgumentParser(description='Publish to PyPI.')
parser.add_argument('--tag', metavar='TAG', type=str, default='',
                    help='git tag corresponding to the version to publish')
args = parser.parse_args()
args.tag = args.tag.strip()
if not args.tag:
    git_head_tags = subprocess.run(
        'git tag -l --points-at HEAD'.split(' '),
        capture_output=True,
        text=True
    ).stdout.strip().split()
    if not git_head_tags:
        raise Exception('Git HEAD has no associated tag')
    elif len(git_head_tags) > 1:
        raise Exception('Git HEAD has multiple tags: '
                        + ', '.join('"{}"'.format(t) for t in git_head_tags))
    args.tag = git_head_tags[0]
assert args.tag
print('\nPublishing version "{}" on PyPI\n'.format(args.tag))

# get internal artifacts repository url
with io.open(Path.home() / '.pip' / 'pip.conf', 'r', encoding='utf-8') as fin:
    repo_url = re.search(
        r'^index-url = (?P<url>.+)$',
        fin.read(),
        flags=re.MULTILINE
    ).group('url')
    repo_url = urlunsplit(
        urlsplit(repo_url)._replace(path='', query='', fragment='')
    )

# get artifact url corresponding to the version to publish
artifact_url = None
components_api = '/service/rest/beta/components?repository=bromine'
r = requests.get(urljoin(repo_url, components_api))
while not artifact_url:
    r = r.json()
    match = [i for i in r['items'] if i['version'] == args.tag]
    if match:
        artifact_data = match[0]['assets'][0]
        artifact_url = urljoin(repo_url, '/repository/bromine/' + artifact_data['path'])
        artifact_sha256 = artifact_data['checksum']['sha256']
    else:
        token = r['continuationToken']
        if token:
            r = requests.get(urljoin(repo_url, components_api + '&continuationToken=' + token))
        else:
            break
assert artifact_url, 'No artifact found for tag "{}" on internal repository.'.format(args.tag)

artifact_url_split = urlsplit(artifact_url)
if '@' in artifact_url_split.netloc:
    netloc = artifact_url_split.netloc.split('@', 1)[1]
    artifact_url_split = artifact_url_split._replace(netloc='***:***@' + netloc)
printable_artifact_url = urlunsplit(artifact_url_split)
print('Downloading artifact "{}"'.format(printable_artifact_url))

# download artifact
tempdir = tempfile.mkdtemp()
filename = PurePath(urlsplit(artifact_url).path).name
filepath = Path(tempdir) / filename
with io.open(filepath, 'w+b') as fout:
    with requests.get(artifact_url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=None):
            fout.write(chunk)
with io.open(filepath, 'rb') as fin:
    sha256 = hashlib.sha256(fin.read()).hexdigest()
    assert sha256 == artifact_sha256, 'Downloaded artifact is corrupted'
print('Artifact downloaded to "{}"'.format(filepath))

# upload artifact to pypi
cmd = 'twine upload {}'.format(filepath)
print('Running:', cmd)
result = subprocess.run(cmd.split(), capture_output=True, text=True)
if result.stdout:
    print(result.stdout)
if result.stderr:
    print(result.stderr)
if result.returncode == 0:
    print('\nSuccess: Bromine "{}" published on PyPI'.format(args.tag))
else:
    print('\nFailed with retcode "{}"'.format(result.returncode))
