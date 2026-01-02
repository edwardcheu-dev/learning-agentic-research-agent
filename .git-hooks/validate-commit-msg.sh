#!/usr/bin/env bash
# Validate commit message prefix

commit_msg_file="$1"

if [ -f "$commit_msg_file" ]; then
    commit_msg=$(cat "$commit_msg_file")
else
    commit_msg="$1"
fi

if ! echo "$commit_msg" | grep -qE "^(test|feat|fix|refactor|docs|chore):"; then
    echo "ERROR: Commit message must start with one of: test:, feat:, fix:, refactor:, docs:, chore:"
    echo "Your message: $commit_msg"
    exit 1
fi

exit 0
