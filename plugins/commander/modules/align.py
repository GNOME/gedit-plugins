# -*- coding: utf-8 -*-
#
#  align.py - align commander module
#
#  Copyright (C) 2010 - Jesse van den Kieboom
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

import commander.commands as commands
import commander.commands.completion
import commander.commands.result
import commander.commands.exceptions

from functools import reduce
import re

__commander_module__ = True

def _get_groups(m, group, add_ws_group):
    if len(m.groups()) <= group - 1:
        gidx = 0
    else:
        gidx = group

    if len(m.groups()) <= add_ws_group - 1:
        wsidx = 0
    else:
        wsidx = add_ws_group

    # Whitespace group must be contained in align group
    if m.start(wsidx) < m.start(gidx) or m.end(wsidx) > m.end(gidx):
        wsidx = gidx

    return (gidx, wsidx)

class Line:
    def __init__(self, line, reg, tabwidth):
        self.tabwidth = tabwidth
        self.line = line

        # All the separators
        self.matches = list(reg.finditer(line))

        # @newline initially contains the first column

        if not self.matches:
            # No separator found
            self.newline = str(line)
        else:
            # Up to first separator
            self.newline = line[0:self.matches[0].start(0)]

    def matches_len(self):
        return len(self.matches)

    def new_len(self, extra=''):
        return len((self.newline + extra).expandtabs(self.tabwidth))

    def match(self, idx):
        if idx >= self.matches_len():
            return None

        return self.matches[idx]

    def append(self, idx, num, group, add_ws_group):
        m = self.match(idx)

        if m == None:
            return

        gidx, wsidx = _get_groups(m, group, add_ws_group)

        # Append leading match
        self.newline += self.line[m.start(0):m.start(gidx)]

        # Now align by replacing wsidx with spaces
        prefix = self.line[m.start(gidx):m.start(wsidx)]
        suffix = self.line[m.end(wsidx):m.end(gidx)]
        sp = ''

        while True:
            bridge = prefix + sp + suffix

            if self.new_len(bridge) < num:
                sp += ' '
            else:
                break

        self.newline += bridge

        # Then append the rest of the match
        mnext = self.match(idx + 1)

        if mnext == None:
            endidx = None
        else:
            endidx = mnext.start(0)

        self.newline += self.line[m.end(gidx):endidx]

    def __str__(self):
        return self.newline

def _find_max_align(lines, idx, group, add_ws_group):
    num = 0

    # We will align on 'group', by adding spaces to 'add_ws_group'
    for line in lines:
        m = line.match(idx)

        if m != None:
            gidx, wsidx = _get_groups(m, group, add_ws_group)

            # until the start
            extra = line.line[m.start(0):m.start(wsidx)] + line.line[m.end(wsidx):m.end(gidx)]

            # Measure where to align it
            l = line.new_len(extra)
        else:
            l = line.new_len()

        if l > num:
            num = l

    return num

def _regex(view, reg, group, additional_ws, add_ws_group, flags=0):
    buf = view.get_buffer()

    # Get the selection of lines to align columns on
    bounds = buf.get_selection_bounds()

    if not bounds:
        start = buf.get_iter_at_mark(buf.get_insert())
        start.set_line_offset(0)

        end = start.copy()

        if not end.ends_line():
            end.forward_to_line_end()

        bounds = (start, end)

    if not bounds[0].equal(bounds[1]) and bounds[1].starts_line():
        bounds[1].backward_line()

        if not bounds[1].ends_line():
            bounds[1].forward_to_line_end()

    # Get the regular expression from the user
    if reg == None:
        reg, words, modifier = (yield commander.commands.result.Prompt('Regex:'))

    # Compile the regular expression
    try:
        reg = re.compile(reg, flags)
    except Exception as e:
        raise commander.commands.exceptions.Execute('Failed to compile regular expression: %s' % (e,))

    # Query the user to provide a regex group number to align on
    if group == None:
        group, words, modifier = (yield commander.commands.result.Prompt('Group (1):'))

    try:
        group = int(group)
    except:
        group = 1

    # Query the user for additional whitespace to insert for separating items
    if additional_ws == None:
        additional_ws, words, modifier = (yield commander.commands.result.Prompt('Additional whitespace (0):'))

    try:
        additional_ws = int(additional_ws)
    except:
        additional_ws = 0

    # Query the user for the regex group number on which to add the
    # whitespace
    if add_ws_group == None:
        add_ws_group, words, modifier = (yield commander.commands.result.Prompt('Whitespace group (1):'))

    try:
        add_ws_group = int(add_ws_group)
    except:
        add_ws_group = -1

    # By default, add the whitespace on the group on which the columns are
    # aligned
    if add_ws_group < 0:
        add_ws_group = group

    start, end = bounds

    if not start.starts_line():
        start.set_line_offset(0)

    if not end.ends_line():
        end.forward_to_line_end()

    lines = start.get_text(end).splitlines()
    newlines = []
    num = 0
    tabwidth = view.get_tab_width()

    # Construct Line objects for all the lines
    newlines = [Line(line, reg, tabwidth) for line in lines]

    # Calculate maximum number of matches (i.e. columns)
    num = reduce(lambda x, y: max(x, y.matches_len()), newlines, 0)

    for i in range(num):
        al = _find_max_align(newlines, i, group, add_ws_group)

        for line in newlines:
            line.append(i, al + additional_ws, group, add_ws_group)

    # Replace lines
    aligned = str.join('\n', [x.newline for x in newlines])

    buf.begin_user_action()
    buf.delete(bounds[0], bounds[1])

    m = buf.create_mark(None, bounds[0], True)

    buf.insert(bounds[1], aligned)
    buf.select_range(buf.get_iter_at_mark(m), bounds[1])
    buf.delete_mark(m)

    buf.end_user_action()

    yield commander.commands.result.DONE

def __default__(view, reg='\s+', align_group=1, padding=1, padding_group=-1):
    """Align selected in columns using a regular expression: align.regex [&lt;regex&gt;=<i>\s+</i>] [&lt;align-group&gt;] [&lt;padding&gt;] [&lt;padding-group&gt;=<i>&lt;align-group&gt;</i>]

Align the selected text in columns separated by the specified regular expression.

The optional &lt;align-group&gt; argument specifies on which group in the regular expression
the text should be aligned and defaults to 1 (or 0 in the case that there is
no explicit group specified). The &lt;align-group&gt; will be <b>replaced</b>
with whitespace to align the columns. The optional &lt;padding&gt; argument can
be used to add additional whitespace to the column separation. The last
optional argument (&lt;padding-group&gt;) can be used to specify a separate
group (which must be contained in &lt;align-group&gt;) which to replace with
whitespace.

The regular expression will be matched in case-sensitive mode"""

    yield _regex(view, reg, align_group, padding, padding_group)

def i(view, reg='\s+', align_group=1, padding=1, padding_group=-1):
    """Align selected in columns using a regular expression: align.regex [&lt;regex&gt;=<i>\s+</i>] [&lt;align-group&gt;] [&lt;padding&gt;] [&lt;padding-group&gt;=<i>&lt;align-group&gt;</i>]

Align the selected text in columns separated by the specified regular expression.

The optional &lt;align-group&gt; argument specifies on which group in the regular expression
the text should be aligned and defaults to 1 (or 0 in the case that there is
no explicit group specified). The &lt;align-group&gt; will be <b>replaced</b>
with whitespace to align the columns. The optional &lt;padding&gt; argument can
be used to add additional whitespace to the column separation. The last
optional argument (&lt;padding-group&gt;) can be used to specify a separate
group (which must be contained in &lt;align-group&gt;) which to replace with
whitespace.

The regular expression will be matched in case-insensitive mode"""

    yield _regex(view, reg, align_group, padding, padding_group, re.IGNORECASE)

# ex:ts=4:et
