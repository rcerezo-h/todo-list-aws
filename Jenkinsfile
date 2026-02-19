pipeline {
  agent none

  environment {
    AWS_REGION = 'us-east-1'
    CONFIG_REPO_RAW_BASE = 'https://raw.githubusercontent.com/rcerezo-h/todo-list-aws-config'
  }

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {

    stage('Checkout (code + config production)') {
      agent { label 'built-in' }
      steps {
        cleanWs()
        checkout scm

        sh """
          set -e
          echo "Descargando samconfig.toml (production) desde repo config..."
          curl -sSL -o samconfig.toml "${CONFIG_REPO_RAW_BASE}/production/samconfig.toml"
          echo "samconfig.toml (production) OK. Primeras lineas:"
          head -n 25 samconfig.toml || true
        """

        sh '''
          echo "=== CONTEXTO ==="
          whoami
          hostname
          echo "BRANCH_NAME=$BRANCH_NAME"
          echo "GIT_BRANCH=$GIT_BRANCH"
          echo "==============="
        '''

        stash name: 'repo', includes: '**', useDefaultExcludes: false
      }
    }

    stage('Build + Deploy PRODUCTION') {
      agent { label 'built-in' }
      steps {
        cleanWs()
        unstash 'repo'

        sh '''
          echo "=== BUILT-IN (PROD DEPLOY) ==="
          whoami
          hostname
          echo "=============================="
        '''

        sh '''
          set -e
          sam validate --region "${AWS_REGION}"
          sam build
          ENVIRONMENT=production bash pipelines/common-steps/deploy.sh
        '''

        script {
          def apiUrl = sh(
            script: """
              aws cloudformation describe-stacks \
                --stack-name todo-list-aws-production \
                --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue | [0]" \
                --region ${AWS_REGION} \
                --output text
            """,
            returnStdout: true
          ).trim()

          writeFile file: 'prod_url.txt', text: apiUrl + "\n"
          echo "PROD URL => ${apiUrl}"

          stash name: 'prod-url', includes: 'prod_url.txt'
        }
      }
    }

    stage('API Tests PRODUCTION (readonly)') {
      agent { label 'api-agent' }
      steps {
        cleanWs()
        unstash 'repo'
        unstash 'prod-url'

        sh '''
          echo "=== API AGENT (PROD READONLY) ==="
          whoami
          hostname
          echo "================================="
        '''

        script {
          def apiUrl = readFile('prod_url.txt').trim()
          withEnv(["BASE_URL=${apiUrl}"]) {
            sh '''
              set -e
              python3 -m pip install --user pytest requests
              export PATH="$HOME/.local/bin:$PATH"
              python3 -m pytest -s --junitxml=rest-prod.xml test/integration/todoApiReadOnlyTest.py
            '''
          }
        }
      }

      post {
        always {
          script {
            if (fileExists('rest-prod.xml')) {
              junit 'rest-prod.xml'
            } else {
              echo 'No se generó rest-prod.xml'
            }
          }
        }
      }
    }
  }
}
