from subprocess import PIPE, Popen

main_branch = 'hw4'
ex = 0
print(f'SkakovLabO4ka {main_branch}')

branch, _ = Popen(["git", "branch"], cwd='SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
for i in branch.decode().split('\n'):
    if main_branch not in i and '*' in i:
        out, _ = Popen(["git", "checkout", main_branch], cwd = 'SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
        print(f'Change branch to {main_branch}.')
        ex = 1

status, _ = Popen(["git", "pull"], cwd='SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
if 'Already up to date.' not in status.decode():
    print('Update program.')
    ex = 1

if ex:
    print('Please restart the program.')
    exit()
