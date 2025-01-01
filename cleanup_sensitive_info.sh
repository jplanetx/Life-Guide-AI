#!/bin/bash

# Remove sensitive files
find . -name "*.env" -delete
find . -name "*secret*" -delete
find . -name "*key*" -delete

# Scan for potential leaks
grep -r "sk-" .
grep -r "ntn_" .
grep -r "api_key" .

# Suggest manual review
echo "Please manually review the above outputs for any remaining sensitive information"
