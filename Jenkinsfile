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
        echo 'TODO: Build'
        sh '''docker --version
docker-compose --version

docker-compose build'''
      }
    }
    stage('Deploy') {
      steps {
        // sh 'docker-machine help'
        // FIXME: Fetch *.pem in a more secure way
        sh '''#/bin/bash

AWS_KEY=hackathon_droidcon.pem
# DEBUG
if [ ! -e  ${AWS_KEY} ]; then
    curl -o ${AWS_KEY} https://gist.githubusercontent.com/gmacario/b2285d6347ec7c9c4954856a93958b1d/raw/4559359b4b8926217f10881c30b35fc39f9b1f7a/hackaton_droidcon.pem
    chmod 600 ${AWS_KEY}
    ls -la ${AWS_KEY}
    sha256sum ${AWS_KEY}
fi
# ???
ssh-keygen
ssh -i ${AWS_KEY} ubuntu@52.212.172.20 sh -c "pwd; id; ls -la; df -h"

# EOF
'''
        // sh 'ssh -i "hackaton_droidcon.pem" ubuntu@52.212.172.20 "pwd; id; ls -la; df -h"'
      }
    }
  }
}
