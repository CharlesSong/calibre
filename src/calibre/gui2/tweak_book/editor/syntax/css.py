#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'

import re

from calibre.gui2.tweak_book.editor import SyntaxTextCharFormat
from calibre.gui2.tweak_book.editor.syntax.base import SyntaxHighlighter

space_pat = re.compile(r'[ \n\t\r\f]+')
cdo_pat = re.compile(r'/\*')
sheet_tokens = [(re.compile(k), v, n) for k, v, n in [
    (r'\:[a-zA-Z0-9_-]+', 'pseudo_selector', 'pseudo-selector'),
    (r'\.[a-zA-Z0-9_-]+', 'class_selector', 'class-selector'),
    (r'\#[a-zA-Z0-9_-]+', 'id_selector', 'id-selector'),
    (r'@[a-zA-Z0-9_-]+', 'preproc', 'atrule'),
    (r'[a-zA-Z0-9_-]+', 'tag', 'tag'),
    (r'[~\^\*!%&\[\]\(\)<>\|+=@:;,./?-]', 'operator', 'operator'),
]]

content_tokens = [(re.compile(k), v, n) for k, v, n in [
    (r'url\(.*?\)', 'string', 'url'),
    (r'@\S+', 'preproc', 'at-rule'),
    (r'(azimuth|background-attachment|background-color|'
    r'background-image|background-position|background-repeat|'
    r'background|border-bottom-color|border-bottom-style|'
    r'border-bottom-width|border-left-color|border-left-style|'
    r'border-left-width|border-right|border-right-color|'
    r'border-right-style|border-right-width|border-top-color|'
    r'border-top-style|border-top-width|border-bottom|'
    r'border-collapse|border-left|border-width|border-color|'
    r'border-spacing|border-style|border-top|border|caption-side|'
    r'clear|clip|color|content|counter-increment|counter-reset|'
    r'cue-after|cue-before|cue|cursor|direction|display|'
    r'elevation|empty-cells|float|font-family|font-size|'
    r'font-size-adjust|font-stretch|font-style|font-variant|'
    r'font-weight|font|height|letter-spacing|line-height|panose-1|'
    r'list-style-type|list-style-image|list-style-position|'
    r'list-style|margin-bottom|margin-left|margin-right|'
    r'margin-top|margin|marker-offset|marks|max-height|max-width|'
    r'min-height|min-width|opacity|orphans|outline|outline-color|'
    r'outline-style|outline-width|overflow(?:-x|-y)?|padding-bottom|'
    r'padding-left|padding-right|padding-top|padding|'
    r'page-break-after|page-break-before|page-break-inside|'
    r'pause-after|pause-before|pause|pitch|pitch-range|'
    r'play-during|position|quotes|richness|right|size|'
    r'speak-header|speak-numeral|speak-punctuation|speak|'
    r'speech-rate|stress|table-layout|text-align|text-decoration|'
    r'text-indent|text-shadow|text-transform|top|unicode-bidi|'
    r'vertical-align|visibility|voice-family|volume|white-space|'
    r'widows|width|word-spacing|z-index|bottom|left|'
    r'above|absolute|always|armenian|aural|auto|avoid|baseline|'
    r'behind|below|bidi-override|blink|block|bold|bolder|both|'
    r'capitalize|center-left|center-right|center|circle|'
    r'cjk-ideographic|close-quote|collapse|condensed|continuous|'
    r'crop|crosshair|cross|cursive|dashed|decimal-leading-zero|'
    r'decimal|default|digits|disc|dotted|double|e-resize|embed|'
    r'extra-condensed|extra-expanded|expanded|fantasy|far-left|'
    r'far-right|faster|fast|fixed|georgian|groove|hebrew|help|'
    r'hidden|hide|higher|high|hiragana-iroha|hiragana|icon|'
    r'inherit|inline-table|inline|inset|inside|invert|italic|'
    r'justify|katakana-iroha|katakana|landscape|larger|large|'
    r'left-side|leftwards|level|lighter|line-through|list-item|'
    r'loud|lower-alpha|lower-greek|lower-roman|lowercase|ltr|'
    r'lower|low|medium|message-box|middle|mix|monospace|'
    r'n-resize|narrower|ne-resize|no-close-quote|no-open-quote|'
    r'no-repeat|none|normal|nowrap|nw-resize|oblique|once|'
    r'open-quote|outset|outside|overline|pointer|portrait|px|'
    r'relative|repeat-x|repeat-y|repeat|rgb|ridge|right-side|'
    r'rightwards|s-resize|sans-serif|scroll|se-resize|'
    r'semi-condensed|semi-expanded|separate|serif|show|silent|'
    r'slow|slower|small-caps|small-caption|smaller|soft|solid|'
    r'spell-out|square|static|status-bar|super|sw-resize|'
    r'table-caption|table-cell|table-column|table-column-group|'
    r'table-footer-group|table-header-group|table-row|'
    r'table-row-group|text|text-bottom|text-top|thick|thin|'
    r'transparent|ultra-condensed|ultra-expanded|underline|'
    r'upper-alpha|upper-latin|upper-roman|uppercase|url|'
    r'visible|w-resize|wait|wider|x-fast|x-high|x-large|x-loud|'
    r'x-low|x-small|x-soft|xx-large|xx-small|yes)\b', 'keyword', 'keyword'),
    (r'(indigo|gold|firebrick|indianred|yellow|darkolivegreen|'
    r'darkseagreen|mediumvioletred|mediumorchid|chartreuse|'
    r'mediumslateblue|black|springgreen|crimson|lightsalmon|brown|'
    r'turquoise|olivedrab|cyan|silver|skyblue|gray|darkturquoise|'
    r'goldenrod|darkgreen|darkviolet|darkgray|lightpink|teal|'
    r'darkmagenta|lightgoldenrodyellow|lavender|yellowgreen|thistle|'
    r'violet|navy|orchid|blue|ghostwhite|honeydew|cornflowerblue|'
    r'darkblue|darkkhaki|mediumpurple|cornsilk|red|bisque|slategray|'
    r'darkcyan|khaki|wheat|deepskyblue|darkred|steelblue|aliceblue|'
    r'gainsboro|mediumturquoise|floralwhite|coral|purple|lightgrey|'
    r'lightcyan|darksalmon|beige|azure|lightsteelblue|oldlace|'
    r'greenyellow|royalblue|lightseagreen|mistyrose|sienna|'
    r'lightcoral|orangered|navajowhite|lime|palegreen|burlywood|'
    r'seashell|mediumspringgreen|fuchsia|papayawhip|blanchedalmond|'
    r'peru|aquamarine|white|darkslategray|ivory|dodgerblue|'
    r'lemonchiffon|chocolate|orange|forestgreen|slateblue|olive|'
    r'mintcream|antiquewhite|darkorange|cadetblue|moccasin|'
    r'limegreen|saddlebrown|darkslateblue|lightskyblue|deeppink|'
    r'plum|aqua|darkgoldenrod|maroon|sandybrown|magenta|tan|'
    r'rosybrown|pink|lightblue|palevioletred|mediumseagreen|'
    r'dimgray|powderblue|seagreen|snow|mediumblue|midnightblue|'
    r'paleturquoise|palegoldenrod|whitesmoke|darkorchid|salmon|'
    r'lightslategray|lawngreen|lightgreen|tomato|hotpink|'
    r'lightyellow|lavenderblush|linen|mediumaquamarine|green|'
    r'blueviolet|peachpuff)\b', 'colorname', 'colorname'),
    (r'\!important', 'preproc', 'important'),
    (r'\#[a-zA-Z0-9]{1,6}', 'number', 'hexnumber'),
    (r'[\.-]?[0-9]*[\.]?[0-9]+(em|px|pt|pc|in|mm|cm|ex|s|rem)\b', 'number', 'dimension'),
    (r'[\.-]?[0-9]*[\.]?[0-9]+%(?=$|[ \n\t\f\r;}{()\[\]])', 'number', 'dimension'),
    (r'-?[0-9]+', 'number', 'number'),
    (r'[~\^\*!%&<>\|+=@:,./?-]+', 'operator', 'operator'),
    (r'[\[\]();]+', 'bracket', 'bracket'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'identifier', 'ident')

]]

class State(object):

    NORMAL = 0
    IN_COMMENT_NORMAL = 1
    IN_SQS = 2
    IN_DQS = 3
    IN_CONTENT = 4
    IN_COMMENT_CONTENT = 5

    def __init__(self, num):
        self.parse  = num & 0b1111
        self.blocks = num >> 4

    @property
    def value(self):
        return ((self.parse & 0b1111) | (max(0, self.blocks) << 4))


def normal(state, text, i, formats):
    ' The normal state (outside content blocks {})'
    m = space_pat.match(text, i)
    if m is not None:
        return [(len(m.group()), None)]
    cdo = cdo_pat.match(text, i)
    if cdo is not None:
        state.parse = State.IN_COMMENT_NORMAL
        return [(len(cdo.group()), formats['comment'])]
    if text[i] == '"':
        state.parse = State.IN_DQS
        return [(1, formats['string'])]
    if text[i] == "'":
        state.parse = State.IN_SQS
        return [(1, formats['string'])]
    if text[i] == '{':
        state.parse = State.IN_CONTENT
        state.blocks += 1
        return [(1, formats['bracket'])]
    for token, fmt, name in sheet_tokens:
        m = token.match(text, i)
        if m is not None:
            return [(len(m.group()), formats[fmt])]

    return [(len(text) - i, formats['unknown-normal'])]

def content(state, text, i, formats):
    ' Inside content blocks '
    m = space_pat.match(text, i)
    if m is not None:
        return [(len(m.group()), None)]
    cdo = cdo_pat.match(text, i)
    if cdo is not None:
        state.parse = State.IN_COMMENT_CONTENT
        return [(len(cdo.group()), formats['comment'])]
    if text[i] == '"':
        state.parse = State.IN_DQS
        return [(1, formats['string'])]
    if text[i] == "'":
        state.parse = State.IN_SQS
        return [(1, formats['string'])]
    if text[i] == '}':
        state.blocks -= 1
        state.parse = State.NORMAL if state.blocks < 1 else State.IN_CONTENT
        return [(1, formats['bracket'])]
    if text[i] == '{':
        state.blocks += 1
        return [(1, formats['bracket'])]
    for token, fmt, name in content_tokens:
        m = token.match(text, i)
        if m is not None:
            return [(len(m.group()), formats[fmt])]

    return [(len(text) - i, formats['unknown-normal'])]

def comment(state, text, i, formats):
    ' Inside a comment '
    pos = text.find('*/', i)
    if pos == -1:
        return [(len(text), formats['comment'])]
    state.parse = State.NORMAL if state.parse == State.IN_COMMENT_NORMAL else State.IN_CONTENT
    return [(pos - i + 2, formats['comment'])]

def in_string(state, text, i, formats):
    'Inside a string'
    q = '"' if state.parse == State.IN_DQS else "'"
    pos = text.find(q, i)
    if pos == -1:
        if text[-1] == '\\':
            # Multi-line string
            return [(len(text) - i, formats['string'])]
        state.parse = (State.NORMAL if state.blocks < 1 else State.IN_CONTENT)
        return [(len(text) - i, formats['unterminated-string'])]
    state.parse = (State.NORMAL if state.blocks < 1 else State.IN_CONTENT)
    return [(pos - i + len(q), formats['string'])]

state_map = {
    State.NORMAL:normal,
    State.IN_COMMENT_NORMAL: comment,
    State.IN_COMMENT_CONTENT: comment,
    State.IN_SQS: in_string,
    State.IN_DQS: in_string,
    State.IN_CONTENT: content,
}

def create_formats(highlighter):
    theme = highlighter.theme
    formats = {
        'comment': theme['Comment'],
        'error': theme['Error'],
        'string': theme['String'],
        'preproc': theme['PreProc'],
        'keyword': theme['Keyword'],
        'colorname': theme['Constant'],
        'number': theme['Number'],
        'operator': theme['Function'],
        'bracket': theme['Special'],
        'identifier': theme['Identifier'],
        'id_selector': theme['Special'],
        'class_selector': theme['Special'],
        'pseudo_selector': theme['Special'],
        'tag': theme['Identifier'],
    }
    for name, msg in {
        'unknown-normal': _('Invalid text'),
        'unterminated-string': _('Unterminated string'),
    }.iteritems():
        f = formats[name] = SyntaxTextCharFormat(formats['error'])
        f.setToolTip(msg)
    return formats


class CSSHighlighter(SyntaxHighlighter):

    state_map = state_map
    state_class = State
    create_formats_func = create_formats

if __name__ == '__main__':
    from calibre.gui2.tweak_book.editor.widget import launch_editor
    launch_editor('''\
@charset "utf-8";
/* A demonstration css sheet */
body {
    color: green;
    font-size: 12pt
}

div#main > a:hover {
    background: url("../image.png");
    font-family: "A font", sans-serif;
}

li[rel="mewl"], p.mewl {
    margin-top: 2% 0 23pt 1em;
}

''', path_is_raw=True, syntax='css')

