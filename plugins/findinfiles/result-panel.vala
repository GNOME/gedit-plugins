/*
* Copyright (C) 2015 The Lemon Man
*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2, or (at your option)
* any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
*/

using Gtk;

namespace Gedit {
namespace FindInFilesPlugin {

void toggle_fold (TreeView tv, TreePath path) {
    if (tv.is_row_expanded (path))
        tv.collapse_row (path);
    else
        tv.expand_row (path, false);
}

class ResultPanel : Overlay {
    // The search job whose results we are showing
    private FindJob job;

    private string root;
    private TreeView list;
    private TreeStore results_model;
    private Button stop_button;
    private Gedit.Window win;

    ~ResultPanel () {
        job.halt ();
    }

    public new void grab_focus () {
        list.grab_focus ();
    }

    // Try to find 'key' anywhere in the path
    private bool list_search (TreeModel model, int column, string key, TreeIter iter) {
        Value val;

        model.get_value (iter, 0, out val);

        // The return values are actually swapped
        return (Posix.strstr (val.get_string (), key) != null) ? false : true;
    }

    private bool on_button_press (Gdk.EventButton event) {
        // Create and show the popup menu on right click
        if (event.type == Gdk.EventType.BUTTON_PRESS && event.button == 3) {
            var popup = new Gtk.Menu ();
            var close_item = new Gtk.MenuItem.with_mnemonic (_("_Close"));

            close_item.activate.connect (() => {
                // Easy peasy
                this.destroy ();
            });

            popup.attach_to_widget (this, null);
            popup.add (close_item);
            popup.show_all ();
            popup.popup (null, null, null, event.button, event.time);

            return true;
        }
        return false;
    }

    private void on_row_activated (TreePath path, TreeViewColumn column) {
        TreeIter iter;
        TreeIter parent;

        if (!results_model.get_iter (out iter, path))
            return;

        // This happens when the user clicks on the file entry
        if (!results_model.iter_parent (out parent, iter)) {
            toggle_fold (list, path);
            return;
        }

        Value val0, val1;
        results_model.get_value (parent, 0, out val0);
        results_model.get_value (iter, 1, out val1);

        var selection_path = val0.get_string (),
            selection_line = val1.get_int ();

        Gedit.commands_load_location (win,
                                      File.new_for_path (selection_path),
                                      null,
                                      selection_line,
                                      0);
    }

    string get_relative_path (string path, string from) {
        // Simplistic way to get a relative path, strip the leading slash too
        if (path.has_prefix (from))
            return path.substring (from.length + 1);

        return path;
    }

    void column_data_func (TreeViewColumn column, CellRenderer cell, TreeModel model, TreeIter iter) {
        TreeIter parent;

        if (!results_model.iter_parent (out parent, iter)) {
            Value val0, val1;

            model.get_value (iter, 0, out val0);
            model.get_value (iter, 1, out val1);

            var path = val0.get_string ();
            var hits = val1.get_int ();

            var hits_text = ngettext ("hit", "hits", hits);
            (cell as CellRendererText).markup = "<b>%s</b> (%d %s)".printf (
                    get_relative_path (path, root),
                    hits,
                    hits_text);
        } else {
            Value val0, val1;

            model.get_value (iter, 0, out val0);
            model.get_value (iter, 1, out val1);

            var at = val1.get_int ();
            var line = val0.get_string ();

            (cell as CellRendererText).text = "%d:%s".printf (at, line);
        }
    }

    public ResultPanel.for_job (FindJob job_, string root_, Gedit.Window win_) {
        results_model = new TreeStore (2, typeof (string), typeof (int));
        job = job_;
        win = win_;
        root = root_;

        var it_table = new HashTable<string, TreeIter?> (str_hash, str_equal);

        // Connect to the job signals
        job.on_match_found.connect((result) => {
            // The 'on_match_found' is emitted from the worker thread
            Idle.add (() => {
                TreeIter iter;

                var parent = it_table.lookup (result.path);

                // Create a new top-level node for the file
                if (parent == null) {
                    results_model.append (out parent, null);
                    results_model.set (parent,
                            0, result.path,
                            1, 0);

                    it_table.insert (result.path, parent);
                }

                // Increment the hits counter
                Value val0;
                results_model.get_value (parent, 1, out val0);
                results_model.set (parent, 1, val0.get_int () + 1);

                // Append the result
                results_model.append (out iter, parent);
                results_model.set (iter,
                                   0, result.context,
                                   1, result.line);

                return false;
            });
        });

        job.on_search_finished.connect (() => {
            job.halt ();
            stop_button.set_visible (false);

            list.expand_all ();

            TreeIter dummy;
            // Check if the search gave no results
            if (!results_model.get_iter_first (out dummy)) {
                results_model.append (out dummy, null);
                results_model.set (dummy, 0, _("No results found"));
            }
        });

        // Create the ui to hold the results
        list = new TreeView.with_model (results_model);

        list.set_search_column (0);
        list.set_search_equal_func (list_search);

        list.insert_column_with_data_func (-1,
                                           "File",
                                           new CellRendererText (),
                                           column_data_func);

        // list.set_activate_on_single_click (true);

        list.row_activated.connect (on_row_activated);
        list.button_press_event.connect (on_button_press);

        // The stop button is showed in the bottom-left corner of the TreeView
        stop_button = new Button.from_icon_name ("process-stop-symbolic", IconSize.BUTTON);
        stop_button.set_tooltip_text (_("Stop the search"));
        stop_button.set_visible (false);
        stop_button.set_valign (Align.END);
        stop_button.set_halign (Align.END);
        stop_button.set_margin_bottom (4);
        stop_button.set_margin_end (4);

        stop_button.clicked.connect (() => {
            stop_button.set_visible (false);
            job.halt ();
        });

        var scroll = new ScrolledWindow (null, null);
        scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        scroll.add (list);

        // The overlay contains the results list and the stop button
        this.add_overlay (stop_button);
        this.add (scroll);
    }

    public void toggle_stop_button (bool show) {
        stop_button.set_visible (show);
    }
}

} // namespace FindInFilesPlugin
} // namespace Gedit
