/*
 * gedit-zeitgeist-plugin.c
 * This file is part of gedit
 *
 * Copyright (C) 2011 - Michal Hruby
 *
 * gedit is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * gedit is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with gedit; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA  02110-1301  USA
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "gedit-zeitgeist-plugin.h"

#include <glib/gi18n.h>
#include <gmodule.h>

#include <gedit/gedit-view.h>
#include <gedit/gedit-view-activatable.h>
#include <gedit/gedit-app.h>
#include <gedit/gedit-app-activatable.h>
#include <gedit/gedit-debug.h>
#include <zeitgeist.h>

enum
{
	SIGNAL_DOC_SAVED,
	SIGNAL_DOC_LOADED,

	N_SIGNALS
};

struct _GeditZeitgeistPluginPrivate
{
	GeditView *view;
	GeditApp  *app;

	gulong     signals[N_SIGNALS];
};

enum
{
	PROP_0,
	PROP_VIEW,
	PROP_APP
};

static void gedit_view_activatable_iface_init (GeditViewActivatableInterface *iface);
static void gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (GeditZeitgeistPlugin,
                                gedit_zeitgeist_plugin,
                                PEAS_TYPE_EXTENSION_BASE,
                                0,
                                G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_VIEW_ACTIVATABLE,
                                                               gedit_view_activatable_iface_init)
                                G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_APP_ACTIVATABLE,
                                                               gedit_app_activatable_iface_init)
				G_ADD_PRIVATE_DYNAMIC (GeditZeitgeistPlugin))

static ZeitgeistLog *zg_log = NULL;
static ZeitgeistDataSourceRegistry *zg_dsr = NULL;

static void
gedit_zeitgeist_plugin_init (GeditZeitgeistPlugin *plugin)
{
	gedit_debug_message (DEBUG_PLUGINS, "GeditZeitgeistPlugin initializing");

	plugin->priv = gedit_zeitgeist_plugin_get_instance_private (plugin);
}

static void
gedit_zeitgeist_plugin_dispose (GObject *object)
{
	GeditZeitgeistPlugin *plugin = GEDIT_ZEITGEIST_PLUGIN (object);

	gedit_debug_message (DEBUG_PLUGINS, "GeditZeitgeistPlugin disposing");

	g_clear_object (&plugin->priv->view);
	g_clear_object (&plugin->priv->app);

	G_OBJECT_CLASS (gedit_zeitgeist_plugin_parent_class)->dispose (object);
}

static void
gedit_zeitgeist_plugin_finalize (GObject *object)
{
	gedit_debug_message (DEBUG_PLUGINS, "GeditZeitgeistPlugin finalizing");

	G_OBJECT_CLASS (gedit_zeitgeist_plugin_parent_class)->finalize (object);
}

static void
gedit_zeitgeist_plugin_set_property (GObject      *object,
				     guint         prop_id,
				     const GValue *value,
				     GParamSpec   *pspec)
{
	GeditZeitgeistPlugin *plugin = GEDIT_ZEITGEIST_PLUGIN (object);

	switch (prop_id)
	{
		case PROP_VIEW:
			plugin->priv->view = GEDIT_VIEW (g_value_dup_object (value));
			break;

		case PROP_APP:
			plugin->priv->app = GEDIT_APP (g_value_dup_object (value));
			break;

		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_zeitgeist_plugin_get_property (GObject    *object,
				     guint       prop_id,
				     GValue     *value,
				     GParamSpec *pspec)
{
	GeditZeitgeistPlugin *plugin = GEDIT_ZEITGEIST_PLUGIN (object);

	switch (prop_id)
	{
		case PROP_VIEW:
			g_value_set_object (value, plugin->priv->view);
			break;

		case PROP_APP:
			g_value_set_object (value, plugin->priv->app);
			break;

		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_zeitgeist_plugin_send_event (GeditZeitgeistPlugin *plugin,
				   GeditDocument *doc, gchar *interpretation)
{
	ZeitgeistEvent *event;
	ZeitgeistSubject *subject;
	GtkSourceFile *file;
	GFile *location;

	file = gedit_document_get_file (doc);
	location = gtk_source_file_get_location (file);

	if (location != NULL)
	{
		gchar *display_name;
		gchar *dir_name;
		gchar *mime_type;
		gchar *doc_uri;

		doc_uri = g_file_get_uri (location);
		dir_name = g_path_get_dirname (doc_uri);
		mime_type = gedit_document_get_mime_type (doc);
		display_name = gedit_document_get_short_name_for_display (doc);

		subject = zeitgeist_subject_new_full (doc_uri,
		                                      ZEITGEIST_NFO_DOCUMENT,
		                                      zeitgeist_manifestation_for_uri (doc_uri),
		                                      mime_type,
		                                      dir_name,
		                                      display_name,
		                                      NULL);

		event = zeitgeist_event_new_full (interpretation,
		                                  ZEITGEIST_ZG_USER_ACTIVITY,
		                                  "application://org.gnome.gedit.desktop",
		                                  NULL,
		                                  subject,
		                                  NULL);

		zeitgeist_log_insert_event_no_reply (zg_log, event, NULL);

		g_free (display_name);
		g_free (mime_type);
		g_free (dir_name);
		g_free (doc_uri);

		g_object_unref (event);
		g_object_unref (subject);
	}
}

static void
document_saved (GeditDocument        *doc,
		GeditZeitgeistPlugin *plugin)
{
	gedit_zeitgeist_plugin_send_event (plugin, doc, ZEITGEIST_ZG_MODIFY_EVENT);
}

static void
document_loaded (GeditDocument        *doc,
		 GeditZeitgeistPlugin *plugin)
{
	gedit_zeitgeist_plugin_send_event (plugin, doc, ZEITGEIST_ZG_ACCESS_EVENT);
}

static void
gedit_zeitgeist_plugin_view_activate (GeditViewActivatable *activatable)
{
	GeditZeitgeistPluginPrivate *priv;
	GeditDocument *doc;

	gedit_debug (DEBUG_PLUGINS);

	priv = GEDIT_ZEITGEIST_PLUGIN (activatable)->priv;

	doc = GEDIT_DOCUMENT (gtk_text_view_get_buffer (GTK_TEXT_VIEW (priv->view)));

	priv->signals[SIGNAL_DOC_SAVED] =
		g_signal_connect (doc,
		                  "saved",
		                  G_CALLBACK (document_saved),
		                  activatable);

	priv->signals[SIGNAL_DOC_LOADED] =
		g_signal_connect (doc,
		                  "loaded",
		                  G_CALLBACK (document_loaded),
		                  activatable);
}

static void
gedit_zeitgeist_plugin_view_deactivate (GeditViewActivatable *activatable)
{
	GeditZeitgeistPluginPrivate *priv;
	GeditDocument *doc;
	int i;

	gedit_debug (DEBUG_PLUGINS);

	priv = GEDIT_ZEITGEIST_PLUGIN (activatable)->priv;

	doc = GEDIT_DOCUMENT (gtk_text_view_get_buffer (GTK_TEXT_VIEW (priv->view)));

	for (i = 0; i < N_SIGNALS; i++)
	{
		g_signal_handler_disconnect (doc, priv->signals[i]);
	}

	gedit_zeitgeist_plugin_send_event (GEDIT_ZEITGEIST_PLUGIN (activatable),
	                                   doc, ZEITGEIST_ZG_LEAVE_EVENT);
}

static void
gedit_zeitgeist_plugin_app_activate (GeditAppActivatable *activatable)
{
	GPtrArray *ptr_arr;
	ZeitgeistEvent *event;
	ZeitgeistDataSource *ds;

	zg_log = zeitgeist_log_new ();

	event = zeitgeist_event_new_full (NULL, NULL,
	                                  "application://org.gnome.gedit.desktop", NULL, NULL);
	ptr_arr = g_ptr_array_new ();
	g_ptr_array_add (ptr_arr, event);
	g_ptr_array_ref (ptr_arr);

	ds = zeitgeist_data_source_new_full ("org.gnome.gedit,dataprovider",
	                                     "Gedit dataprovider",
	                                     "Logs events about accessed documents",
	                                     ptr_arr),

	zg_dsr = zeitgeist_data_source_registry_new ();
	zeitgeist_data_source_registry_register_data_source (zg_dsr, ds,
	                                                     NULL, NULL, NULL);
	g_ptr_array_set_free_func (ptr_arr, g_object_unref);
	g_ptr_array_unref (ptr_arr);
}

static void
gedit_zeitgeist_plugin_app_deactivate (GeditAppActivatable *activatable)
{
	g_object_unref (zg_log);
	g_object_unref (zg_dsr);
}

static void
gedit_zeitgeist_plugin_class_init (GeditZeitgeistPluginClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	object_class->dispose = gedit_zeitgeist_plugin_dispose;
	object_class->finalize = gedit_zeitgeist_plugin_finalize;
	object_class->set_property = gedit_zeitgeist_plugin_set_property;
	object_class->get_property = gedit_zeitgeist_plugin_get_property;

	g_object_class_override_property (object_class, PROP_VIEW, "view");
	g_object_class_override_property (object_class, PROP_APP, "app");
}

static void
gedit_view_activatable_iface_init (GeditViewActivatableInterface *iface)
{
	iface->activate = gedit_zeitgeist_plugin_view_activate;
	iface->deactivate = gedit_zeitgeist_plugin_view_deactivate;
}

static void
gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface)
{
	iface->activate = gedit_zeitgeist_plugin_app_activate;
	iface->deactivate = gedit_zeitgeist_plugin_app_deactivate;
}

static void
gedit_zeitgeist_plugin_class_finalize (GeditZeitgeistPluginClass *klass)
{
}

G_MODULE_EXPORT void
peas_register_types (PeasObjectModule *module)
{
	gedit_zeitgeist_plugin_register_type (G_TYPE_MODULE (module));

	peas_object_module_register_extension_type (module,
	                                            GEDIT_TYPE_VIEW_ACTIVATABLE,
	                                            GEDIT_TYPE_ZEITGEIST_PLUGIN);
	peas_object_module_register_extension_type (module,
	                                            GEDIT_TYPE_APP_ACTIVATABLE,
	                                            GEDIT_TYPE_ZEITGEIST_PLUGIN);
}

/* ex:set ts=8 noet: */
