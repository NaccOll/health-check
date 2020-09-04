import os
path = '.'
env_dir = (path+os.path.sep+'.venv')
for prefix, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.pyc'):
            filename = os.path.join(prefix, name)
            if filename.startswith(env_dir):
                continue
            os.remove(filename)
