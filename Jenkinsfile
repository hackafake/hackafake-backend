pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'INFO: Executing stage Build'
        sh '''#/bin/bash

docker --version
docker-compose --version
docker-compose build --pull

# EOF
'''
      }
    }
    stage('Test') {
      steps {
        echo 'TODO'
      }
    }
    stage('Deploy') {
      steps {
        echo 'INFO: Executing stage Deploy-staging'
        sh 'printenv | sort'
        sh '''#/bin/bash

# Deploy project to remote server

echo "DEBUG: JOB_NAME=${JOB_NAME}"
echo "DEBUG: BRANCH_NAME=${BRANCH_NAME}"

echo "DEBUG: Inspecting host configuration"
id; hostname; pwd; ls -la

if [ "$BRANCH_NAME" = "master" ]; then

  echo "INFO: Deploying to staging server"

  REMOTEUSER=root
  REMOTEHOST=cc-vm3.solarma.it
  REMOTEDIR=/var/tmp/${JOB_NAME}

elif [ "$BRANCH_NAME" = "prod" ]; then

  echo "INFO: Deploying to production server"

  REMOTEUSER=root
  REMOTEHOST=cc-vm4.solarma.it
  REMOTEDIR=/var/tmp/${JOB_NAME}

else

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> No action"
  return
    
fi

echo "DEBUG: Inspecting target configuration"
ssh ${REMOTEUSER}@${REMOTEHOST} "id; hostname; pwd; ls -la"

if [ "${REMOTEUSER}" = "root" ]; then
  echo "INFO: Preparing remote host ${REMOTEHOST}"
  ssh -o StrictHostKeyChecking=no ${REMOTEUSER}@${REMOTEHOST} sh -c "\\
      apt-get update && apt-get -y dist-upgrade && \\
      apt-get -y install git"
  # TODO: Install docker
  # TODO: Install docker-compose
fi

echo "INFO: Deploying container to ${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}"
ssh ${REMOTEUSER}@${REMOTEHOST} "mkdir -p ${REMOTEDIR}"
rsync -avz . "${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}/"
ssh ${REMOTEUSER}@${REMOTEHOST} "cd ${REMOTEDIR} && \\
git log -1 && \\
git status && \\
docker-compose build --pull && \\
docker-compose up -d"

# EOF
'''
      }
    }
  }
}
