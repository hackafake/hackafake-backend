pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'INFO: Executing stage Build'
        sh '''#/bin/bash

docker --version
docker-compose --version
docker-compose build
# EOF
'''
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

  echo "TODO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to staging"

  REMOTEUSER=root
  REMOTEHOST=cc-vm3.solarma.it
  REMOTEDIR=/var/tmp/${BRANCH_NAME}

elif [ "$BRANCH_NAME" = "feature/implement-staging" ]; then

  echo "TODO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to cc-vm2"

  REMOTEUSER=root
  REMOTEHOST=cc-vm2.solarma.it
  REMOTEDIR=/var/tmp/${BRANCH_NAME}

else

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> No action"
  return
    
fi

echo "DEBUG: Inspecting target configuration"
ssh ${ROOT}@${REMOTEHOST} "id; hostname; pwd; ls -la"

echo "INFO: Deploying container to ${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}"
ssh ${REMOTEUSER}@${REMOTEHOST} "mkdir -p ${REMOTEDIR}"
rsync -avz . ${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}/
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