from subprocess import PIPE, Popen

# воронка с master на ветку с актуальной дз.

actual_branch = 'hw4'
ex = 0
print(f'SkakovLabO4ka {actual_branch}')

branch, _ = Popen(["git", "branch"], cwd='SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
for i in branch.decode().split('\n'):
    if actual_branch not in i and '*' in i:
        out, _ = Popen(["git", "checkout", actual_branch], cwd = 'SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
        print(f'Change branch to {actual_branch}.')
        print('Please restart the program.')
        exit()
