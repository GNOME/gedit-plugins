#!/usr/bin/env python3
#
# Gedit Scheme Editor
# https://github.com/jonocodes/GeditSchemer
#
# Copyright (C) Jono Finger 2013 <jono@foodnotblogs.com>
# 
# The program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# The program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.



# please keep these in alphabetical order so it is easy to follow
# see available languages: /usr/share/libgedit-gtksourceview-300/language-specs
# or run in python >>> GtkSource.LanguageManager().get_language_ids()

samples = {}

samples['ada'] = """
with Ada.Text_Io; use Ada.Text_Io;
 
 procedure Doors is
    type Door_State is (Closed, Open);
    type Door_List is array(Positive range 1..100) of Door_State;
    The_Doors : Door_List := (others => Closed);
 begin
    for I in 1..100 loop
       for J in The_Doors'range loop
          if J mod I = 0 then
             if The_Doors(J) = Closed then
                 The_Doors(J) := Open;
             else
                The_Doors(J) := Closed;
             end if;
          end if;
       end loop;
    end loop;
    for I in The_Doors'range loop
       Put_Line(Integer'Image(I) & " is " & Door_State'Image(The_Doors(I)));
    end loop;
 end Doors;
"""

samples['asp'] = """
<html>
<body>
<form action="demo_reqquery.asp" method="get">
Your name: <input type="text" name="fname" size="20" />
<input type="submit" value="Submit" />
</form>
<%
dim fname
fname=Request.QueryString("fname")
If fname<>"" Then
      Response.Write("Hello " & fname & "!<br />")
      Response.Write("How are you today?")
End If
%>
</body>
</html>
"""

# samples['automake'] = """

samples['awk'] = """
BEGIN {
  for(i=1; i <= 100; i++) {
    doors[i] = 0 # close the doors
  }
  for(i=1; i <= 100; i++) {
    if ( int(sqrt(i)) == sqrt(i) ) {
      doors[i] = 1
    }
  }
  for(i=1; i <= 100; i++)
  {
    print i, doors[i] ? "open" : "close"
  }
}
"""

# samples['bennugd'] = """
# samples['bibtex'] = """
# samples['boo'] = """

# do not remove this language since it is the fallback entry
samples['c'] = """
/* Some comments */
#include <stdio.h>
 
int main()
{
  int square = 1, increment = 3, door;
  for (door = 1; door <= 100; ++door)
  {
    printf("door #%d", door);
    if (door == square)
    {
      printf(" is open.");
      square += increment;
      increment += 2;
    }
    else
      printf(" is closed.");
  }
  return 0;
}
"""

samples['c-sharp'] ="""
// Creates and initializes a new integer Array
int[] intArray = new int[5] { 1, 2, 3, 4, 5 };
//same as
int[] intArray = new int[]{ 1, 2, 3, 4, 5 };
//same as
int[] intArray = { 1, 2, 3, 4, 5 };
 
//Arrays are zero-based
string[] stringArr = new string[5];
stringArr[0] = "string";
"""

# samples['cg'] = """
# samples['changelog'] = """
# samples['chdr'] = """
# samples['cmake'] = """
# samples['cobol'] = """
# samples['cpp'] = """
# samples['css'] = """
# samples['cuda'] = """
# samples['d'] = """
# samples['def'] = """
# samples['desktop'] = """

samples['diff'] = """
--- xinetd.d/tftp       2003-12-17 13:11:20.000000000 -0500
+++ ./tftp      2004-01-22 11:46:14.479497688 -0500
@@ -10,7 +10,7 @@
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
-       server_args             = -s /tftpboot
+       server_args             = -p -u tftpd -s /tftpboot
        disable                 = yes
        per_source              = 11
        cps                     = 100 2
"""
# samples['docbook'] = """
# samples['dosbatch'] = """
# samples['dot'] = """
# samples['dpatch'] = """
# samples['dtd'] = """
# samples['eiffel'] = """
# samples['erlang'] = """
# samples['fcl'] = """
# samples['forth'] = """
# samples['fortran'] = """
# samples['fsharp'] = """
# samples['gap'] = """
# samples['gdb-log'] = """
# samples['gettext-translation'] = """
# samples['glsl'] = """
# samples['go'] = """
# samples['gtk-doc'] = """
# samples['gtkrc'] = """
# samples['haddock'] = """
# samples['haskell'] = """
# samples['haskell-literate'] = """

samples['html'] = """
<html>
<body>

<table border="1">
  <caption>Monthly savings</caption>
  <tr>
    <th>Month</th>
    <th>Savings</th>
  </tr>
  <tr>
    <td>January</td>
    <td>$100</td>
  </tr>
  <tr>
    <td>February</td>
    <td>$50</td>
  </tr>
</table>

</body>
</html>
"""

# samples['idl'] = """
# samples['imagej'] = """
# samples['ini'] = """
# samples['java'] = """
# samples['js'] = """
# samples['json'] = """
# samples['latex'] = """
# samples['libtool'] = """
# samples['lua'] = """
# samples['m4'] = """
# samples['makefile'] = """
# samples['mallard'] = """
# samples['markdown'] = """
# samples['matlab'] = """
# samples['nemerle'] = """
# samples['nsis'] = """
# samples['objc'] = """
# samples['objective-caml'] = """
# samples['objj'] = """
# samples['ocl'] = """
# samples['octave'] = """
# samples['ooc'] = """
# samples['opal'] = """
# samples['opencl'] = """
# samples['pascal'] = """
# samples['perl'] = """

samples['php'] = """
/* ygtyuy */
print 'hello world';
"""
# samples['pkgconfig'] = """
# samples['prolog'] = """
# samples['proto'] = """

samples['python'] = """
  def on_save_clicked(self, param):
    if not self.currentSchemeFile:
      
      filename = runSaveAsDialog(self.window, self.entryId.get_text() + '.xml')
    
      if filename and not '.' in os.path.basename(filename):
        filename = filename + '.xml'
      
      if filename:
        self.write_scheme(filename, self.entryId.get_text())
        self.currentSchemeFile = filename
    
    else:
      self.write_scheme(self.currentSchemeFile, self.entryId.get_text())
      
      # TODO handle case where there is a permissions issue
"""

# samples['r'] = """
# samples['rpmspec'] = """
# samples['ruby'] = """
# samples['scheme'] = """
# samples['scilab'] = """
# samples['sh'] = """
# samples['sml'] = """
# samples['sparql'] = """
# samples['sql'] = """
# samples['systemverilog'] = """
# samples['t2t'] = """
# samples['tcl'] = """
# samples['texinfo'] = """
# samples['vala'] = """
# samples['vbnet'] = """
# samples['verilog'] = """
# samples['vhdl'] = """
# samples['xml'] = """
# samples['xslt'] = """
# samples['yacc'] = """
