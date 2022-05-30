from subprocess import PIPE, Popen


status, _ = Popen(["git", "pull"], cwd='SkakovLabO4ka', stdout = PIPE, stderr = PIPE).communicate()
if 'Already up to date.' not in status.decode():
    print('Update program.')
    print('Please restart the program.')
    exit()
