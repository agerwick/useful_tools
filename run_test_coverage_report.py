from useful_tools.generate_test_coverage_report import generate_test_coverage_report
generate_test_coverage_report(
    minimum_test_coverage_percentage = 80, # commit will fail if test coverage is below this threshold
    allow_commit_to_any_branch = False, # if True, restricted_branches will be ignored (for temporary use only)
    restricted_branches = ['main'], # branches you can't commit to but you have to use pull requests instead
    branches_with_enforced_test_coverage = ['dev', 'main'], # branches where the test coverage is enforced -- should include restricted_branches, in case allow_commit_to_any_branch is True
    code_locations = ['.'], # where application code is located
    exclude_code_locations = ['tests'], # if any code locations should be excluded, for example if tests are located a subdirectory of the code location
    test_code_locations = ['tests'] # where test code is located
)
