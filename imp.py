from os import listdir
import re
import fontforge
import os.path

inpath = "/home/nekoyasha/Desktop/nekotoba2/"
exp = re.compile(r"U\+(.*)\.svg")

af = fontforge.activeFont()
print af

bunch = listdir(inpath)
for f in bunch:
    m = exp.match(f)
    if m:
        print f, m.group(1)
        g = af.createChar(int(m.group(1),16))
        print g
        if not g.isWorthOutputting():
            p = os.path.join(inpath,f)
            print p
            g.importOutlines(p)
            g.simplify(2.4, ("ignoreslopes", "ignoreextrema", "smoothcurves"))
            g.addExtrema("only_good_rm")
            g.removeOverlap()
            g.correctDirection()
            g.round()
            #remove small splines here
            g.addExtrema("all")
            g.canonicalContours()
            g.round()
            g.removeOverlap()
            g.round()
            #fix width here
            g.width = af.em
            g.validate(True)


