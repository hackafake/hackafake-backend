pipeline {
  agent any
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
        sh 'docker-machine help'
      }
    }
  }
}