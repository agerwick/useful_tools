#!/bin/bash
# check if .venv exists
if [ -d ".venv" ]; then
    echo ".venv exists"
else
    echo "Please create a virtual environment first"
    echo "You can use this command: python3 -m venv .venv"
    exit 1
fi
# check if .venv is activated
if [ "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is activated"
else
    echo "Please activate the virtual environment first"
    echo "You can use this command: source .venv/bin/activate"
    exit 1
fi
# check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt exists"
else
    echo "requirements.txt does not exist - please create it first"
    echo "If it does exist, you might be in the wrong directory."
    echo "Current directory: $(pwd)"
    echo "You should be in your projet's root directory."
    exit 1
fi
# check if coverage is in requirements.txt
if grep -q "coverage" "requirements.txt"; then
    echo "coverage is already in requirements.txt"
else
    echo "coverage is not in requirements.txt -- adding it now"
    echo "coverage" >> requirements.txt
    exit 1
fi
# check if git+https://github.com/agerwick/useful_tools.git is in requirements.txt
if grep -q "git+https://github.com/agerwick/useful_tools.git" "requirements.txt"; then
    echo "useful_tools is already in requirements.txt"
else
    echo "useful_tools is not in requirements.txt -- adding it now"
    echo "git+https://github.com/agerwick/useful_tools.git" >> requirements.txt
fi
# check if the generate_test_coverage_report.example directory exists
if [ -d ".venv/lib/site-packages/useful_tools/generate_test_coverage_report_files" ]; then
    echo ".venv/lib/site-packages/useful_tools/generate_test_coverage_report_files exists"
else
    echo ".venv/lib/site-packages/useful_tools/generate_test_coverage_report_files does not exist -- it should have been installed with the useful_tools package"
    echo "You may need to run 'pip install -r ./requirements.txt'."
    exit 1
fi
# check if the .coveragerc file exists
if [ -f ".coveragerc" ]; then
    echo ".coveragerc already exists -- no need to copy it"
else
    echo "copying .coveragerc"
    cp .venv/lib/site-packages/useful_tools/generate_test_coverage_report_files/.coveragerc .coveragerc
fi
# check if the .githooks directory exists
if [ -d ".githooks" ]; then
    echo ".githooks already exists -- no need to copy it"
else
    echo "copying .githooks"
    cp -r .venv/lib/site-packages/useful_tools/generate_test_coverage_report_files/.githooks .githooks
fi
# check if the run_test_coverage_report.py file exists
if [ -f "run_test_coverage_report.py" ]; then
    echo "run_test_coverage_report.py already exists -- no need to copy it"
else
    echo "copying run_test_coverage_report.py"
    cp .venv/lib/site-packages/useful_tools/generate_test_coverage_report_files/run_test_coverage_report.py run_test_coverage_report.py
fi
echo "Adding .githooks folder to github hooks path..."
git config core.hooksPath .githooks
echo "making run_test_coverage_report.sh executable..."
chmod +x .githooks/pre-commit
echo "installation complete"
