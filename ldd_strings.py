import subprocess
import sys

string = "/usr/bin/strings"

def get_linked_objs(binary):
    args = ["/usr/bin/otool", "-L", binary]
    res = subprocess.check_output(args).split("\n")
    res = res[1:]
    objs = []

    for i in res:
        x = i.lstrip()
        x = x.split(" ")[0]
        objs.append(x)

    return objs

def pprint(binary, res):

    print "\033[0;32mIn %s\033[0m" % binary
    for i in res.split("\n"):
        print "\t%s" % i
    print

def strings_and_grep(binary, needle):
    st = subprocess.Popen((string, binary), stdout=subprocess.PIPE)
    try:
        grep = subprocess.check_output(("/usr/bin/grep", needle), stdin=st.stdout)
    except:
        grep = None
    st.wait()

    if grep and needle in grep:
        pprint(binary, grep)

def doit(binary, needle):
    print "Checking binary itself:\n"

    strings_and_grep(binary, needle)
    print "Checking dependencies\n\n"
    for i in get_linked_objs(binary):
        if i:
            strings_and_grep(i, needle)

print
if len(sys.argv) < 3:
    print 'expecting two arguments, binary and what to grep for'
    sys.exit(1)

if len(sys.argv) == 4 and sys.argv[3] == "nm":
    string = "/usr/bin/nm"


binary = sys.argv[1]
needle = sys.argv[2]

doit(binary, needle)







