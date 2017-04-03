#! /usr/bin/env python3
# -*- mode: python; -*-

import argparse, html, json, os, sys

# so this script needs to find cellomap.{html,css,js} when run, either
# relative to itself or in some standard location - sigh - not again.

def arguments():
    parser = argparse.ArgumentParser(description = '''
    Turn a JSON set of labeled points into an interactive viewer
    of the points in cells laid over a rectangular region of an
    underlying map. Outliers will be clamped into the cells.''')
    parser.add_argument('--xmin', default = 0.0, type = float, help = 'minimum x-coordinate')
    parser.add_argument('--xmax', default = 1.0, type = float, help = 'maximum x-coordinate')
    parser.add_argument('--ymin', default = 0.0, type = float, help = 'minimum y-coordinate')
    parser.add_argument('--ymax', default = 1.0, type = float, help = 'maximum y-coordinate')
    parser.add_argument('data', help = 'JSON file')
    return parser.parse_args()

def pieces(self):
    home = os.path.dirname(self)
    page = open(os.path.join(home, 'cellomap.html')).read()
    style = open(os.path.join(home, 'cellomap.css')).read()
    code = open(os.path.join(home, 'cellomap.js')).read()
    return page, style, code

def midwid(begin, end):
    '''Let user adjust a range (in case the data is not distributed as expected),
    by controlling midpoint or width of the range to a limited extent.'''

    if not begin < end: raise Exception()
    wid = end - begin
    mid = begin + wid/2
    minmid, maxmid = begin - wid/2, end + wid/2
    minwid, maxwid = wid/2, wid * 2
    return minmid, mid, maxmid, minwid, wid, maxwid

def checkdata(data):
    pass

def main():
    args = arguments()

    data = json.load(open(args.data))
    page, style, code = pieces(sys.argv[0])
    checkdata(data)

    minmx, mx, maxmx, minwx, wx, maxwx = midwid(args.xmin, args.xmax)
    minmy, my, maxmy, minwy, wy, maxwy = midwid(args.ymin, args.ymax)
    page = page.format(MinMidX = minmx, MaxMidX = maxmx, ValMidX = mx,
                       MinWidX = minwx, MaxWidX = maxwx, ValWidX = wx,
                       MinMidY = minmy, MaxMidY = maxmy, ValMidY = my,
                       MinWidY = minwy, MaxWidY = maxwy, ValWidY = wy,
                       StepMidX = (maxmx - minmx) / 10,
                       StepWidX = (maxwx - minwx) / 10,
                       StepMidY = (maxmy - minmy) / 10,
                       StepWidY = (maxwy - minwy) / 10)

    data = ',\n'.join(json.dumps(datum, ensure_ascii = False)
                      for datum in data)
    data = html.escape(data, quote = False)
    page = page.replace('<!--[DATA]-->', data)

    style = '\n'.join(('<style>',
                       html.escape(style, quote = False),
                       '</style>'))
    #   <link href="cellomap.css" rel="stylesheet">
    page = page.replace('<!--[STYLE]-->', style)

    #  <script type="text/javascript" src="cellomap.js"></script>
    # oh - one does not escape this? then data above should also not be!
    # what about style then?
    code = '\n'.join(('<script>', code, '</script>'))
    page = page.replace('<!--[CODE]-->', code)

    print(page)

if __name__ == '__main__':
    main()
