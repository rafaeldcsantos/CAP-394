#!/bin/bash

# Rerun quarto
sass Resources/CSS/custom.scss Resources/CSS/custom.css
quarto render --to html

