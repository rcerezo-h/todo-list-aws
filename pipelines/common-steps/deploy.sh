#!/bin/bash
set -euo pipefail
set -x

du -hs * | sort -h

ENVIRONMENT="${ENVIRONMENT:-staging}"

sam deploy \
	  --template-file .aws-sam/build/template.yaml \
	    --config-file samconfig.toml \
	      --config-env "$ENVIRONMENT" \
	        --no-confirm-changeset \
		  --force-upload \
		    --no-fail-on-empty-changeset \
		      --no-progressbar

