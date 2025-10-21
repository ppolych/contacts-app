pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  triggers { pollSCM('@hourly') }  // ή webhook καλύτερα

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build images') {
      steps {
        sh 'docker compose -f docker-compose.yml build'
      }
    }

    // Προαιρετικά: lint/tests αν έχεις
    // stage('Tests') {
    //   steps {
    //     sh 'docker compose run --rm web pytest || true'
    //   }
    // }

    stage('Package') {
      steps {
        sh 'docker images | head -n 20'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '**/logs/**', allowEmptyArchive: true
      cleanWs()
    }
  }
}
