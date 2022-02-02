import subprocess
def call(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    O = ''
    E = ''
    while p.poll() is None:
        tmp = p.stdout.read(1)
        if tmp:
            O += tmp
        tmp = p.stderr.read(1)
        if tmp:
            E += tmp
    ret = p.poll(), O+p.stdout.read(), E+p.stderr.read() # Catch remaining output
    p.stdout.close() # Always close your file handles, or your OS might be pissed
    p.stderr.close()
    return ret