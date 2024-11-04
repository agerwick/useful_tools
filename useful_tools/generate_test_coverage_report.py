import os
import sys
import glob
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

# installation:
# assumes:
# - you have git installed and initialized in your project
# - you have a virtual environment set up in .env/
# - you are in the root folder of your project
# pip install coverage
# pip install git+https://github.com/agerwick/useful_tools.git
# mkdir .githooks
# cp .venv/lib/site-packages/useful_tools/generate_test_coverage_report.example/* .
# git config core.hooksPath .githooks
# chmod +x .githooks/pre-commit
# edit run_test_coverage_report.py to set the minimum_test_coverage_percentage, etc.
# both run_test_coverage_report.py and the .githooks folder should be committed to the repository
# add these two lines to your readme, so that other developers know how to set up the pre-commit hook
# git config core.hooksPath .githooks
# chmod +x .githooks/pre-commit

# usage:
# when committing, the pre-commit hook will run the test coverage report
# if the branch is restricted, the commit will be aborted - you will need to use pull requests instead
# if the branch is in branches_with_enforced_test_coverage, and the test coverage is below the threshold, the commit will be aborted
# otherwise the commit will proceed
# regardless of the outcome, the test coverage report will saved in coverage_stats.txt

# this entire script is not covered by tests, because it is meant to be run as a pre-commit hook, and testing it requires running coverage.py, which is already being run by this script... so to prevent infinite recursion, and retain my sanity, we will not test this script
def generate_test_coverage_report( # pragma: no cover
    minimum_test_coverage_percentage=None, 
    allow_commit_to_any_branch=None,
    restricted_branches=[],
    branches_with_enforced_test_coverage=[],
    code_locations=[],
    exclude_code_locations=[],
    test_code_locations=[]
):
    if not isinstance(minimum_test_coverage_percentage, int):
        raise ValueError('generate_test_coverage_report: Please provide a value for minimum_test_coverage_percentage (e.g. 85 for 85%)')
    if not isinstance(allow_commit_to_any_branch, bool):
        raise ValueError('generate_test_coverage_report: Please provide a value for allow_commit_to_any_repo (True or False)')
    if not isinstance(restricted_branches, list) or not restricted_branches:
        raise ValueError('generate_test_coverage_report: Please provide a list of restricted branches, typically ["main", "test"]')
    if not isinstance(branches_with_enforced_test_coverage, list) or not branches_with_enforced_test_coverage:
        raise ValueError('generate_test_coverage_report: Please provide a list of branches with enforced test coverage, typically ["dev", "test", "main"]')
    if not isinstance(code_locations, list) or not code_locations:
        raise ValueError('generate_test_coverage_report: Please provide a list of code locations')
    if not isinstance(exclude_code_locations, list):
        raise ValueError('generate_test_coverage_report: Please provide a list of code locations to exclude')
    if not isinstance(test_code_locations, list) or not test_code_locations:
        raise ValueError('generate_test_coverage_report: Please provide a list of test code locations')

    # Important note when modifying this script:
    # if it returns a non-zero exit code, the commit will be aborted, 
    # and the error message will be the first line of output from this script
    # Hence, make sure that first line is useful and informative

    # Disabled as it does not give accurate results
    # # Function to count lines of code in a directory
    # def count_lines_of_code(directory, extension="*.py"):
    #     total_lines = 0
    #     for filepath in glob.glob(os.path.join(directory, '**', extension), recursive=True):
    #         with open(filepath, 'r', encoding='utf-8') as file:
    #             total_lines += sum(1 for line in file)
    #     return total_lines

    # find the path to the python executable
    python_path = sys.executable
    coverage_path = os.path.join(os.path.dirname(python_path), 'coverage')

    # Run the coverage commands
    process = subprocess.run([coverage_path, 'run', '-m', 'pytest'], capture_output=True, text=True)
    if process.returncode != 0:
        print('ERROR: Coverage run failed -- please check the output below:')
        print(process.stdout)
        print(process.stderr)

    process = subprocess.run([coverage_path, 'xml'], capture_output=True, text=True)
    if process.returncode != 0:
        print('ERROR: Coverage xml generation failed -- please check the output below:')
        print(process.stdout)
        print(process.stderr)

    # Parse the coverage.xml file
    tree = ET.parse('coverage.xml')
    root = tree.getroot()

    # Extract the required information
    coverage_version = root.attrib['version']
    timestamp = int(root.attrib['timestamp']) / 1000  # Convert to seconds
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    lines_valid = root.attrib['lines-valid']
    lines_covered = root.attrib['lines-covered']
    test_coverage = float(root.attrib['line-rate']) * 100  # Convert to percentage
    # Disabled as it does not give accurate results
    # # go through all code locations to count number of lines of code that should be tested
    # total_lines_of_code = 0
    # for code_location in code_locations:
    #     total_lines_of_code += count_lines_of_code(code_location)
    # # remove lines of code that should be excluded from the test coverage calculation
    # for exclude_code_location in exclude_code_locations:
    #     total_lines_of_code -= count_lines_of_code(exclude_code_location)
    # # go through all test locations to count number of lines of test code
    # total_lines_of_test_code = 0
    # for test_code_location in test_code_locations:
    #     total_lines_of_test_code += count_lines_of_code(test_code_location)

    git_branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()

    # Write the information to coverage_stats.txt
    with open('coverage_stats.txt', 'w') as f:
        f.write(f'coverage version:                          {coverage_version}\n')
        f.write(f'time report was generated:                 {datetime_str}\n')
        # f.write(f'total lines of code:                       {total_lines_of_code}\n') # Disabled as it does not give accurate results
        f.write(f'total lines of code that should be tested: {lines_valid}\n')
        f.write(f'total lines of code covered by tests:      {lines_covered}\n')
        # f.write(f'total lines of test code:                  {total_lines_of_test_code}\n') # Disabled as it does not give accurate results
        f.write(f'total test coverage:                       {test_coverage:.2f}%\n')
        f.write(f'test coverage threshold:                   {minimum_test_coverage_percentage}%\n')
        # # Disabled as it does not give accurate results
        # # calculate ratio of lines of test code vs lines of code that should be tested
        # test_coverage_ratio = total_lines_of_test_code / int(lines_valid)
        # f.write(f'ratio of test code to app code:            {test_coverage_ratio:.2f}:1\n')

    severity_level = None
    if test_coverage < minimum_test_coverage_percentage:
        if git_branch in branches_with_enforced_test_coverage:
            severity_level = "ERROR"
        else:
            severity_level = "WARNING"

    def print_coverage_message():
        if test_coverage < minimum_test_coverage_percentage:
            print(f'\n{severity_level}: Current test coverage of {test_coverage:.2f}% is below required threshold of {minimum_test_coverage_percentage}%.')
        else:
            print(f'Current test coverage of {test_coverage:.2f}% meets the required threshold of {minimum_test_coverage_percentage}%.')
        print('You can find the coverage report in coverage_stats.txt\n')

    if git_branch in restricted_branches and not allow_commit_to_any_branch:
        print(f'ERROR: You cannot commit directly to the {git_branch} branch.')
        print()
        print('Create a feature branch, then merge to dev.')
        print('  Use the format "FEATURE/XXX-nnn" where XXX is the project code and nnn is the issue number.')
        print('  For example, "FEATURE/MIM-123" for issue 123 in the MIM project.')
        print()
        print_coverage_message()
        print()
        print('After merging to dev, create a pull request to merge to test.')
        print('After testing is complete, create a pull request to merge to main.')
        print()
        sys.exit(1) # Exit with an error code, causing .git/hooks/pre-commit to fail

    if severity_level: # either "ERROR" or "WARNING"
        print_coverage_message()
    print(f'Current git branch: {git_branch}')

    print()
    # Print the contents of coverage_stats.txt to the console
    with open('coverage_stats.txt', 'r') as f:
        print(f.read())

    if test_coverage < minimum_test_coverage_percentage:
        if git_branch in branches_with_enforced_test_coverage:
            sys.exit(1) # Exit with an error code, causing .git/hooks/pre-commit to fail

    sys.exit(0) # Exit with a success code, allowing the commit to proceed

pass