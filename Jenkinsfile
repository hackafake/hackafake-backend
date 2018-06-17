pipeline {
  // agent {
  //   docker {
  //     // TRYME: https://github.com/silinternational/ecs-deploy
  //     image 'gmacario/android-devenv:latest'
  //   }
  // }
  //
  agent any
  //
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
        echo 'INFO: Executing stage Deploy'
        // sh 'docker-machine help'
        // DEBUG: Display environment variables
        sh 'printenv | sort'
        // TODO: Identify the envvar containing the git branch name
        // FIXME: Fetch *.pem in a more secure way
        sh '''#/bin/bash
        
# Deploy project to remote server

echo "DEBUG: BRANCH_NAME=${BRANCH_NAME}"

if [ "$BRANCH_NAME" == "master" ]; then

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to staging"

AWS_KEY=hackathon_droidcon.pem
# DEBUG
if [ ! -e  ${AWS_KEY} ]; then
    curl -o ${AWS_KEY} https://gist.githubusercontent.com/gmacario/b2285d6347ec7c9c4954856a93958b1d/raw/4559359b4b8926217f10881c30b35fc39f9b1f7a/hackaton_droidcon.pem
    chmod 600 ${AWS_KEY}
    ls -la ${AWS_KEY}
    sha256sum ${AWS_KEY}
fi

# ssh -o StrictHostKeyChecking=no -i ${AWS_KEY} ubuntu@52.212.172.20 sh -c "pwd; id; ls -la; df -h"

ssh -o StrictHostKeyChecking=no -i ${AWS_KEY} ubuntu@52.212.172.20 sh -c "\
id && \
pwd && \
cd /home/ubuntu/github/SOLARMA/hackafake-backend && \
git pull --all --prune && \
git log -1 && \
git status && \
docker-compose build --pull && \
docker-compose up -d"

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

elif [ "$BRANCH_NAME" == "prod" ]; then

  echo "INFO: BRANCH_NAME=${BRANCH_NAME} ==> Deploying to production"

else

  echo "WARNING: BRANCH_NAME=${BRANCH_NAME} ==> No action"
    
fi

# EOF
'''
        // sh 'ssh -i "hackaton_droidcon.pem" ubuntu@52.212.172.20 "pwd; id; ls -la; df -h"'
      }
    }
  }
}
