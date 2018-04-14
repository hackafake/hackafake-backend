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
        sh 'ssh -i "hackaton_droidcon.pem" ubuntu@52.212.172.20 "pwd; id; ls -la; df -h"'
      }
    }
  }
}
