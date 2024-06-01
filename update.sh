#!/bin/bash

# Rerun quarto
sass Resources/CSS/custom.scss Resources/CSS/custom.css
quarto render --to html --verbose


# Add all changes
git add .

# Commit changes with a default message
git commit -m "Update changes"

# Push changes to the main branch
git push origin main
