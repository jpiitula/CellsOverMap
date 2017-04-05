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
    parser.add_argument('--xmin', type = float, help = 'minimum x-coordinate')
    parser.add_argument('--xmax', type = float, help = 'maximum x-coordinate')
    parser.add_argument('--ymin', type = float, help = 'minimum y-coordinate')
    parser.add_argument('--ymax', type = float, help = 'maximum y-coordinate')
    parser.add_argument('data', help = 'JSON file')
    return parser.parse_args()

def pieces(self):
    home = os.path.dirname(self)
    page = open(os.path.join(home, 'cellomap.html')).read()
    style = open(os.path.join(home, 'cellomap.css')).read()
    code = open(os.path.join(home, 'cellomap.js')).read()
    return page, style, code

def load(filename):
    '''Returns the data, or exits with a message in stderr if there are
    problems loading the data or the data is not as expected.'''

    try:
        data = json.load(open(filename))
    except ValueError:
        print('Unexpected data:',
              'could not load data as JSON',
              file = sys.stderr)
        exit(1)

    if not isinstance(data, list):
        print('Unexpected data:',
              'not a list',
              file = sys.stderr)
        exit(1)

    try:
        for label, x, y, o in data:
            if not isinstance(label, str): raise ValueError()
            if not isinstance(x, (int, float)): raise ValueError()
            if not isinstance(y, (int, float)): raise ValueError()
            if not isinstance(o, dict): raise ValueError()
            if not all(isinstance(v, str) for v in o.values()): raise ValueError()
    except ValueError:
        print('Unexpected data:',
              'a datum is not a list [label, x, y, { key : value, ... }]',
              'containing a string, two numbers, and a key-value mapping',
              'where each value is a string',
              sep = '\n',
              file = sys.stderr)
        exit(1)

    return data

def limits(data, args):
    '''Return xmin, xmax, ymin, ymax for data. Could do something more
    clever later but this will have to do as limits for now.'''

    if data:
        xmin = min(x for u, x, y, o in data) if args.xmin is None else args.xmin
        xmax = max(x for u, x, y, o in data) if args.xmax is None else args.xmax
        ymin = min(y for u, x, y, o in data) if args.ymin is None else args.ymin
        ymax = max(y for u, x, y, o in data) if args.ymax is None else args.ymax
    else:
        xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin, args.ymax

    # should check here that all four limits are reasonable - would
    # have been easier to insist on some data and not allow user to
    # set limits at all - oh, must also insist on non-empty ranges!

    return xmin, xmax, ymin, ymax

def middle(begin, end):
    '''Return the minimum and maximum for a midpoint range. Let HTML set
    the default midpoint at the middle by default and allow "any" step
    there.'''

    if not begin < end: raise ValueError()
    midmin = begin - (end - begin)/2
    midmax = end + (end - begin)/2
    return midmin, midmax

def width(begin, end):
    '''Return the minimum and maximum for a width range. Choose them so
    that default width is at the middle, and let HTML set it there by
    default; allow "any" step there.'''

    if not begin < end: raise ValueError()
    widmin = 0.25 * (end - begin)
    widmax = 1.75 * (end - begin)
    return widmin, widmax

def main():
    args = arguments()

    data = load(args.data)

    page, style, code = pieces(sys.argv[0])

    xmin, xmax, ymin, ymax = limits(data, args)
    mxmin, mxmax = middle(xmin, xmax)
    mymin, mymax = middle(ymin, ymax)
    wxmin, wxmax = width(xmin, xmax)
    wymin, wymax = width(ymin, ymax)
    page = page.format(MinMidX = mxmin, MaxMidX = mxmax,
                       MinWidX = wxmin, MaxWidX = wxmax,
                       MinMidY = mymin, MaxMidY = mymax,
                       MinWidY = wymin, MaxWidY = wymax)

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
