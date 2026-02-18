#!/bin/bash
set -euo pipefail
set -x
ENVIRONMENT="${ENVIRONMENT:-production}"
STACK_NAME="todo-list-aws-${ENVIRONMENT}"
STACK_NAME="${STACK_NAME:-todo-list-aws-${ENVIRONMENT}}"

du -hs * | sort -h

ENVIRONMENT="${ENVIRONMENT:-staging}"

sam deploy --template-file .aws-sam/build/template.yaml \
	  --config-file samconfig.toml \
	    --config-env "${ENVIRONMENT}" \
	      --stack-name "${STACK_NAME}" \
	        --region "${AWS_REGION}" \
		--resolve-s3 \
		  --no-confirm-changeset \
		    --force-upload \
		      --no-fail-on-empty-changeset \
		        --no-progressbar

