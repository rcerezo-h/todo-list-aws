pipeline {
  agent none

  environment {
    AWS_REGION = 'us-east-1'
    GIT_CREDENTIALS_ID = 'github-token-user'
    CONFIG_REPO_RAW_BASE = 'https://raw.githubusercontent.com/rcerezo-h/todo-list-aws-config'
  }

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {

    stage('Checkout (code + config staging)') {
      agent { label 'built-in' }
      steps {
        cleanWs()
        checkout scm

        sh """
          set -e
          echo "Descargando samconfig.toml (staging) desde repo config..."
          curl -sSL -o samconfig.toml "${CONFIG_REPO_RAW_BASE}/staging/samconfig.toml"
          echo "samconfig.toml (staging) OK. Primeras lineas:"
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

    stage('Static Analysis (Flake8 + Bandit)') {
      agent { label 'static-agent' }
      steps {
        cleanWs()
        unstash 'repo'

        sh '''
          echo "=== STATIC AGENT ==="
          whoami
          hostname
          echo "==================="
        '''

        sh '''
          set -e
          python3 -m pip install --user flake8 bandit
          export PATH="$HOME/.local/bin:$PATH"

          python3 -m flake8 src --exit-zero --format=pylint > flake8.out
          python3 -m bandit -r src -f custom -o bandit.out \
            --msg-template "{abspath}:{line}: [{test_id}] {msg}" || true
        '''

        archiveArtifacts artifacts: 'flake8.out, bandit.out', fingerprint: true
      }
    }

    stage('Build + Deploy STAGING') {
      agent { label 'built-in' }
      steps {
        cleanWs()
        unstash 'repo'

        sh '''
          echo "=== BUILT-IN (STAGING DEPLOY) ==="
          whoami
          hostname
          echo "================================="
        '''

        sh '''
          set -e
          sam validate --region "${AWS_REGION}"
          sam build
          ENVIRONMENT=staging bash pipelines/common-steps/deploy.sh
        '''

        script {
          def apiUrl = sh(
            script: """
              aws cloudformation describe-stacks \
                --stack-name todo-list-aws-staging \
                --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue | [0]" \
                --region ${AWS_REGION} \
                --output text
            """,
            returnStdout: true
          ).trim()

          writeFile file: 'staging_url.txt', text: apiUrl + "\n"
          echo "STAGING URL => ${apiUrl}"

          stash name: 'staging-url', includes: 'staging_url.txt'
        }
      }
    }

    stage('API Tests STAGING (pytest)') {
      agent { label 'api-agent' }
      steps {
        cleanWs()
        unstash 'repo'
        unstash 'staging-url'

        sh '''
          echo "=== API AGENT (STAGING TESTS) ==="
          whoami
          hostname
          echo "================================="
        '''

        script {
          def apiUrl = readFile('staging_url.txt').trim()
          withEnv(["BASE_URL=${apiUrl}"]) {
            sh '''
              set -e
              python3 -m pip install --user pytest requests
              export PATH="$HOME/.local/bin:$PATH"
              python3 -m pytest -s --junitxml=rest-staging.xml test/integration/todoApiTest.py
            '''
          }
        }
      }

      post {
        always {
          script {
            if (fileExists('rest-staging.xml')) {
              junit 'rest-staging.xml'
            } else {
              echo 'No se generó rest-staging.xml'
            }
          }
        }
      }
    }

    stage('Promote: merge develop -> master') {
      agent { label 'built-in' }
      steps {
        cleanWs()
        checkout scm

        sh '''
          echo "=== BUILT-IN (MERGE) ==="
          whoami
          hostname
          echo "========================"
        '''

        withCredentials([usernamePassword(
          credentialsId: env.GIT_CREDENTIALS_ID,
          usernameVariable: 'GIT_USER',
          passwordVariable: 'GIT_TOKEN'
        )]) {
          sh '''
            set -eux

            git fetch origin +refs/heads/develop:refs/remotes/origin/develop +refs/heads/master:refs/remotes/origin/master

            git checkout -B develop origin/develop
            git checkout -B master  origin/master

            git checkout master
          # Identidad para commits de merge
            git config user.email "jenkins@local"
            git config user.name "Jenkins"
          
            # Si hay conflicto (por el Jenkinsfile), conserva el de master
            git merge develop -X ours --no-edit
          
            REPO="$(git config remote.origin.url | sed 's#https://##')"
            git remote set-url origin "https://${GIT_USER}:${GIT_TOKEN}@${REPO}"
            git push origin master
          '''
        }
      }
    }
  }
}