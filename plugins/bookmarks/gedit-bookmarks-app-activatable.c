/*
 * gedit-bookmarks-app-activatable.c
 * This file is part of gedit
 *
 * Copyright (C) 2014 - Ignacio Casal Quinteiro
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
 * along with gedit. If not, see <http://www.gnu.org/licenses/>.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <glib/gi18n-lib.h>
#include <gedit/gedit-app.h>
#include <gedit/gedit-app-activatable.h>
#include <libpeas/peas-object-module.h>
#include "gedit-bookmarks-app-activatable.h"

typedef struct _GeditBookmarksAppActivatablePrivate
{
	GeditApp *app;
	GeditMenuExtension *menu_ext;
} GeditBookmarksAppActivatablePrivate;

enum
{
	PROP_0,
	PROP_APP
};

static void gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (GeditBookmarksAppActivatable,
                                gedit_bookmarks_app_activatable,
                                G_TYPE_OBJECT,
                                0,
                                G_ADD_PRIVATE_DYNAMIC (GeditBookmarksAppActivatable)
                                G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_APP_ACTIVATABLE,
                                                               gedit_app_activatable_iface_init))

static void
gedit_bookmarks_app_activatable_dispose (GObject *object)
{
	GeditBookmarksAppActivatable *activatable = GEDIT_BOOKMARKS_APP_ACTIVATABLE (object);
	GeditBookmarksAppActivatablePrivate *priv = gedit_bookmarks_app_activatable_get_instance_private (activatable);

	g_clear_object (&priv->app);
	g_clear_object (&priv->menu_ext);

	G_OBJECT_CLASS (gedit_bookmarks_app_activatable_parent_class)->dispose (object);
}

static void
gedit_bookmarks_app_activatable_set_property (GObject      *object,
                                              guint         prop_id,
                                              const GValue *value,
                                              GParamSpec   *pspec)
{
	GeditBookmarksAppActivatable *activatable = GEDIT_BOOKMARKS_APP_ACTIVATABLE (object);
	GeditBookmarksAppActivatablePrivate *priv = gedit_bookmarks_app_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_APP:
			priv->app = GEDIT_APP (g_value_dup_object (value));
			break;

		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_bookmarks_app_activatable_get_property (GObject    *object,
                                              guint       prop_id,
                                              GValue     *value,
                                              GParamSpec *pspec)
{
	GeditBookmarksAppActivatable *activatable = GEDIT_BOOKMARKS_APP_ACTIVATABLE (object);
	GeditBookmarksAppActivatablePrivate *priv = gedit_bookmarks_app_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_APP:
			g_value_set_object (value, priv->app);
			break;

		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_bookmarks_app_activatable_class_init (GeditBookmarksAppActivatableClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	object_class->dispose = gedit_bookmarks_app_activatable_dispose;
	object_class->set_property = gedit_bookmarks_app_activatable_set_property;
	object_class->get_property = gedit_bookmarks_app_activatable_get_property;

	g_object_class_override_property (object_class, PROP_APP, "app");
}

static void
gedit_bookmarks_app_activatable_class_finalize (GeditBookmarksAppActivatableClass *klass)
{
}

static void
gedit_bookmarks_app_activatable_init (GeditBookmarksAppActivatable *self)
{
}

static void
gedit_bookmarks_app_activatable_activate (GeditAppActivatable *activatable)
{
	GeditBookmarksAppActivatable *app_activatable = GEDIT_BOOKMARKS_APP_ACTIVATABLE (activatable);
	GeditBookmarksAppActivatablePrivate *priv = gedit_bookmarks_app_activatable_get_instance_private (app_activatable);
	GMenuItem *item;
	const gchar *toggle_accel[] = {"<Primary><Alt>B", NULL};
	const gchar *next_others_accel[] = {"<Primary>B", NULL};
	const gchar *prev_accel[] = {"<Primary><Shift>B", NULL};

	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-toggle", toggle_accel);
	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-next", next_others_accel);
	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-prev", prev_accel);

	priv->menu_ext = gedit_app_activatable_extend_menu (activatable, "search-section");
	item = g_menu_item_new (_("Toggle Bookmark"), "win.bookmark-toggle");
	gedit_menu_extension_append_menu_item (priv->menu_ext, item);
	g_object_unref (item);

	item = g_menu_item_new (_("Goto Next Bookmark"), "win.bookmark-next");
	gedit_menu_extension_append_menu_item (priv->menu_ext, item);
	g_object_unref (item);

	item = g_menu_item_new (_("Goto Previous Bookmark"), "win.bookmark-prev");
	gedit_menu_extension_append_menu_item (priv->menu_ext, item);
	g_object_unref (item);
}

static void
gedit_bookmarks_app_activatable_deactivate (GeditAppActivatable *activatable)
{
	GeditBookmarksAppActivatable *app_activatable = GEDIT_BOOKMARKS_APP_ACTIVATABLE (activatable);
	GeditBookmarksAppActivatablePrivate *priv = gedit_bookmarks_app_activatable_get_instance_private (app_activatable);
	const gchar *accels[] = { NULL };

	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-toggle", accels);
	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-next", accels);
	gtk_application_set_accels_for_action (GTK_APPLICATION (priv->app), "win.bookmark-prev", accels);

	g_clear_object (&priv->menu_ext);
}

static void
gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface)
{
	iface->activate = gedit_bookmarks_app_activatable_activate;
	iface->deactivate = gedit_bookmarks_app_activatable_deactivate;
}

void
gedit_bookmarks_app_activatable_register (GTypeModule *module)
{
	gedit_bookmarks_app_activatable_register_type (module);

	peas_object_module_register_extension_type (PEAS_OBJECT_MODULE (module),
	                                            GEDIT_TYPE_APP_ACTIVATABLE,
	                                            GEDIT_TYPE_BOOKMARKS_APP_ACTIVATABLE);
}

/* ex:ts=8:noet: */
