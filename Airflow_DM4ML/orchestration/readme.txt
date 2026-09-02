//Install

pip install dvc
dvc init


//Track datasets

dvc add data/raw
dvc add data/processed
dvc add data/features

// Commit

git add data.dvc .gitignore
git commit -m "Version raw, processed, and feature data"

