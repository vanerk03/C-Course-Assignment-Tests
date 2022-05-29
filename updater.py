from subprocess import PIPE, Popen

main_branch = 'hw3'
ex = 0
print(f'SkakovLabO4ka {main_branch}')

branch, _ = Popen(["git", "branch"], cwd='SkakovLabO4ka', stdout = PIPE).communicate()
for i in branch.decode().split('\n'):
    if main_branch in i and '*' not in i:
        out, _ = Popen(["git", "checkout", main_branch], cwd = 'SkakovLabO4ka', stdout = PIPE).communicate()
        print(f'Change branch to {main_branch}.')
        ex = 1

status, _ = Popen(["git", "pull"], cwd='SkakovLabO4ka', stdout = PIPE).communicate()
if 'Already up to date.' not in status.decode():
    print('Update program.')
    ex = 1

if ex:
    print('Please restart the program.')
    exit()
