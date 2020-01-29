node {
    stage('Git Checkout') {
        sh 'if [ -d ".git" ]; then git clean -ffdx; fi'
        checkout scm

        if (env.BRANCH_NAME.startsWith('release/')) {
            sh 'sed -i "s/_BUILD//g" src/bromine/_version.py'
        } else {
            sh 'sed -i "s/_BUILD/.dev${BUILD_NUMBER}/g" src/bromine/_version.py'
        }
        sh 'sed -i "s/COMMIT/$(git log -n 1 --pretty=format:\"%h\")/g" src/bromine/_version.py'
    }
    stage('Bdist Wheel') {
        docker.image('python:3.8').inside('-v /etc/passwd:/etc/passwd') {
            sh """
            python3 -m venv /tmp/venv
            . /tmp/venv/bin/activate
            pip install -U --no-cache-dir -r requirements/build.txt
            make clean
            python setup.py bdist_wheel --universal
            """
        }
    }
    /*stage('GPG Sign') {
        withCredentials([string(credentialsId: 'jenkins_gpg_0780E4BA_pwd', variable: 'PASSWORD')]) {
            sh 'gpg --detach-sign -a --batch --passphrase "$PASSWORD" dist/bromine-*.whl'
        }
    }
    stage('QA - Verify Signature') {
        sh """
        gpg --dearmor <pypi_gpg_sign.pub.asc >pypi_gpg_sign.pub.pgp
        gpg --no-default-keyring --keyring ./pypi_gpg_sign.pub.pgp --verify dist/bromine-*.whl.asc
        """
    }*/
    stage('QA - Test') {
        parallel py38: {
            docker.image('python:3.8').inside('-v /etc/passwd:/etc/passwd') {
                stage('Tox -e py38') {
                    sh """
                    python3 -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --no-cache-dir -r requirements/qa.txt
                    tox -e py38 --installpkg dist/bromine-*.whl --workdir /tmp/venv38
                    """
                }
            }
        }, py37: {
            docker.image('python:3.7').inside('-v /etc/passwd:/etc/passwd') {
                stage('Tox -e py37') {
                    sh """
                    python3 -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --no-cache-dir -r requirements/qa.txt
                    tox -e py37 --installpkg dist/bromine-*.whl --workdir /tmp/venv37
                    """
                }
            }
        }, py36: {
            docker.image('python:3.6').inside('-v /etc/passwd:/etc/passwd') {
                stage('Tox -e py36') {
                    sh """
                    python3 -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --no-cache-dir -r requirements/qa.txt
                    tox -e py36 --installpkg dist/bromine-*.whl --workdir /tmp/venv36
                    """
                }
            }
        }
    }
    stage('QA - Coverage') {
        docker.image('python:3.8').inside('-v /etc/passwd:/etc/passwd') {
            sh """
            python3 -m venv /tmp/venv
            . /tmp/venv/bin/activate
            pip install --no-cache-dir -r requirements/qa.txt
            rm -f .coverage
            coverage combine .coverage_*
            coverage report -m
            """
        }
    }
    stage('QA - Lint') {
        docker.image('python:3.8').inside('-v /etc/passwd:/etc/passwd') {
            sh """
            python3 -m venv /tmp/venv
            . /tmp/venv/bin/activate
            pip install --no-cache-dir -r requirements/qa.txt -r requirements/bromine.txt
            make lint
            """
        }
    }

    if (env.BRANCH_NAME.startsWith("development/") || env.BRANCH_NAME.startsWith("release/")) {
        stage('Publish to Private Nexus') {
            docker.image('python:3.8').inside('-v /etc/passwd:/etc/passwd') {
                withCredentials([
                    usernamePassword(credentialsId: 'nexus-id',
                                     usernameVariable: 'USERNAME',
                                     passwordVariable: 'PASSWORD'),
                    string(credentialsId: 'nexus_url', variable: 'NEXUS_URL')
                ]) {
                    sh """
                    python3 -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --no-cache-dir -r requirements/pypi.txt
                    twine upload --repository-url ${NEXUS_URL}/bromine/ -u $USERNAME -p $PASSWORD dist/bromine-*.whl
                    """
                }
            }
        }

        if (env.BRANCH_NAME.startsWith("release/")) {
            stage('Git Tag') {
                def built_version = sh(returnStdout: true,
                                       script: "ls -1 dist/bromine-*.whl | cut -d '-' -f 2").trim()
                sh """
                git tag ${built_version}
                git push origin ${built_version}
                """
            }
        }
    }
}
