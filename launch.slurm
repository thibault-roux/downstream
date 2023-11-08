#!/bin/bash
#SBATCH --job-name=correlation
#SBATCH --time=05:30:00
#SBATCH --output=output.txt
#xSBATCH --partition=cpu
#qSBATCH --mail-type=END,FAIL


python correlation.py