#!/bin/bash

# Rerun quarto
sassc Resources/CSS/custom.scss Resources/CSS/custom.css
quarto render --to html

