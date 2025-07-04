#!/bin/bash

conda activate DataScience

# Rerun quarto
sassc Resources/CSS/custom.scss Resources/CSS/custom.css
quarto render --to html

