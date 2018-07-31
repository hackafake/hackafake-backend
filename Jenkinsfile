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
    stage('Deploy-staging') {
      steps {
        echo 'INFO: Executing stage Deploy-staging'
        sh 'printenv | sort'
        sh '''#/bin/bash

# Deploy project to remote server

echo "DEBUG: BRANCH_NAME=${BRANCH_NAME}"
if [ "$BRANCH_NAME" = "master" ]; then

  echo "TODO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to staging"

elif [ "$BRANCH_NAME" = "feature/implement-staging" ]; then

  echo "TODO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to cc-vm2"

  echo "DEBUG: Inspecting host configuration"
  id; hostname; pwd; ls -la

  echo "DEBUG: Inspecting target configuration"
  ssh root@cc-vm2.solarma.it "id; hostname; pwd; ls -la"

  REMOTEUSER=root
  REMOTEHOST=cc-vm2.solarma.it
  REMOTEDIR=/var/tmp/${BRANCH_NAME}

  echo "INFO: Deploying container to ${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}"
  ssh ${REMOTEUSER}@${REMOTEHOST} "mkdir -p ${REMOTEDIR}"
  rsync -avz . ${REMOTEUSER}@${REMOTEHOST}:${REMOTEDIR}/
  ssh ${REMOTEUSER}@${REMOTEHOST} "cd ${REMOTEDIR} && \\
  git log -1 && \\
  git status && \\
  docker-compose build --pull && \\
  docker-compose up -d"

else

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> No action"
    
fi

# EOF
'''
      }
    }
    stage('Deploy-prod') {
      steps {
        echo 'INFO: Executing stage Deploy-prod'
        sh '''#/bin/bash
        
# Deploy project to remote server

echo "DEBUG: BRANCH_NAME=${BRANCH_NAME}"

if [ "$BRANCH_NAME" = "prod" ]; then

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to production server"

AWS_KEY=hackathon_droidcon.pem
# DEBUG
if [ ! -e  ${AWS_KEY} ]; then
    curl -o ${AWS_KEY} https://gist.githubusercontent.com/gmacario/b2285d6347ec7c9c4954856a93958b1d/raw/4559359b4b8926217f10881c30b35fc39f9b1f7a/hackaton_droidcon.pem
    chmod 600 ${AWS_KEY}
    ls -la ${AWS_KEY}
    sha256sum ${AWS_KEY}
fi

# ssh -o StrictHostKeyChecking=no -i ${AWS_KEY} ubuntu@52.212.172.20 sh -c "pwd; id; ls -la; df -h"

ssh -o StrictHostKeyChecking=no -i ${AWS_KEY} ubuntu@52.212.172.20 sh -c "id && pwd && cd /home/ubuntu/github/SOLARMA/hackafake-backend && git pull --all --prune && git log -1 && git status && docker-compose build --pull && docker-compose up -d"

# DEBUG
# pwd; id; ls -la; df -h
# docker --version
# docker images
# docker ps
# docker-compose --version
#
# cd github/SOLARMA/hackafake-backend
# git pull --all --prune
# git log -1
# git status
# docker-compose build --pull
# docker-compose up

else

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> No action"
    
fi

# EOF
'''
      }
    }
  }
}