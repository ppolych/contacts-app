// Jenkins declarative pipeline for building the Flask app image and deploying via docker compose
// Comments in English as requested.

pipeline {
  agent any

  environment {
    COMPOSE_PROJECT_NAME = 'contacts_stack'
    APP_IMAGE = 'ppolych/contacts-web:latest'  // change to your Docker Hub if you plan to push
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Docker CLI (if needed)') {
      steps {
        sh 'which docker || (apt-get update && apt-get install -y docker.io)'
        sh 'docker version'
      }
    }

    stage('Build image') {
      steps {
        sh 'docker compose build web'
      }
    }

    stage('Unit tests') {
      steps {
        sh 'echo "No tests yet"'
      }
    }

    stage('Deploy (recreate web)') {
      steps {
        sh 'docker compose up -d --no-deps --build web'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '**/web/*.py', onlyIfSuccessful: false
    }
  }
}
