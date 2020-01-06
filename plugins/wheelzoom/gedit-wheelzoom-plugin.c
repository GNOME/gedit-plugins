/*
 * gedit-wheelzoom-plugin.c
 *
 * Original author: Javier Goday <jgoday@gmail.com>
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
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 */
#include "gedit-wheelzoom-plugin.h"

#include <string.h>
#include <glib/gi18n.h>
#include <gdk/gdk.h>
#include <gtk/gtk.h>

#include <gedit/gedit-debug.h>
#include <gedit/gedit-utils.h>
#include <gedit/gedit-app.h>
#include <gedit/gedit-window.h>
#include <gedit/gedit-app-activatable.h>
#include <gedit/gedit-window-activatable.h>

static void gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface);
static void gedit_window_activatable_iface_init (GeditWindowActivatableInterface *iface);

struct _GeditWheelZoomPluginPrivate
{
	GeditWindow *window;
	GeditApp *app;
	GeditView *view;
};

enum
{
	PROP_0,
	PROP_WINDOW,
	PROP_APP
};

G_DEFINE_DYNAMIC_TYPE_EXTENDED (GeditWheelZoomPlugin,
				gedit_wheelzoom_plugin,
				PEAS_TYPE_EXTENSION_BASE,
				0,
				G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_APP_ACTIVATABLE,
							       gedit_app_activatable_iface_init)
				G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_WINDOW_ACTIVATABLE,
							       gedit_window_activatable_iface_init)
				G_ADD_PRIVATE_DYNAMIC (GeditWheelZoomPlugin))

static gboolean
zoom_it (GtkWidget      *widget,
		 GdkEventScroll *event,
		 GeditAppActivatable *activatable)
{
	int state;

	state = event->state & gtk_accelerator_get_default_mod_mask();

	if (state != GDK_CONTROL_MASK)
	{
		return FALSE;
	}

	GtkStyleContext *ctx;
	PangoFontDescription *font_desc;
	int size, amount;

	if (event->direction == GDK_SCROLL_SMOOTH)
	{
		amount = event->delta_y > 0 ? 1 : -1;
	}
	else if (event->direction == GDK_SCROLL_UP)
	{
		amount = 1;
	}
	else
	{
		amount = -1;
	}

	ctx = gtk_widget_get_style_context (widget);
	gtk_style_context_get (ctx, 
     	gtk_style_context_get_state (ctx),
		"font",
		&font_desc, NULL);

	size = pango_font_description_get_size (font_desc);

	pango_font_description_set_size (font_desc, size + amount * PANGO_SCALE);
	gtk_widget_override_font (widget, font_desc);

	return GDK_EVENT_PROPAGATE;
}

static void
gedit_wheelzoom_plugin_app_activate (GeditAppActivatable *activatable)
{
}

static void
gedit_wheelzoom_plugin_app_deactivate (GeditAppActivatable *activatable)
{
}

static void
gedit_wheelzoom_plugin_window_activate (GeditWindowActivatable *activatable)
{
}

static void
gedit_wheelzoom_plugin_window_deactivate (GeditWindowActivatable *activatable)
{
}

static void
gedit_wheelzoom_plugin_window_update_state (GeditWindowActivatable *activatable)
{
	GeditWheelZoomPluginPrivate *priv;

	priv = GEDIT_WHEELZOOM_PLUGIN (activatable)->priv;
	if (!priv->view)
	{
		priv->view = gedit_window_get_active_view (priv->window);
		if (priv->view)
		{
			g_signal_connect (priv->view, "scroll-event",
							G_CALLBACK (zoom_it), priv->view);
		}
	}
}

static void
gedit_wheelzoom_plugin_init (GeditWheelZoomPlugin *plugin)
{
	plugin->priv = gedit_wheelzoom_plugin_get_instance_private (plugin);
}

static void
gedit_wheelzoom_plugin_dispose (GObject *object)
{
	G_OBJECT_CLASS (gedit_wheelzoom_plugin_parent_class)->dispose (object);
}


static void
gedit_wheelzoom_plugin_finalize (GObject *object)
{
	G_OBJECT_CLASS (gedit_wheelzoom_plugin_parent_class)->finalize (object);
}

static void
gedit_wheelzoom_plugin_set_property (GObject      *object,
               		                 guint         prop_id,
                    	             const GValue *value,
                        	         GParamSpec   *pspec)
{
	GeditWheelZoomPlugin *plugin = GEDIT_WHEELZOOM_PLUGIN (object);

	switch (prop_id)
	{
		case PROP_WINDOW:
			plugin->priv->window = GEDIT_WINDOW (g_value_dup_object (value));
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
gedit_wheelzoom_plugin_get_property (GObject    *object,
                                	 guint       prop_id,
                                	 GValue     *value,
                                	 GParamSpec *pspec)
{
	GeditWheelZoomPlugin *plugin = GEDIT_WHEELZOOM_PLUGIN (object);

	switch (prop_id)
	{
		case PROP_WINDOW:
			g_value_set_object (value, plugin->priv->window);
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
gedit_wheelzoom_plugin_class_init (GeditWheelZoomPluginClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	object_class->dispose = gedit_wheelzoom_plugin_dispose;
	object_class->finalize = gedit_wheelzoom_plugin_finalize;
	object_class->set_property = gedit_wheelzoom_plugin_set_property;
	object_class->get_property = gedit_wheelzoom_plugin_get_property;

	g_object_class_override_property (object_class, PROP_WINDOW, "window");
	g_object_class_override_property (object_class, PROP_APP, "app");
}

static void
gedit_wheelzoom_plugin_class_finalize (GeditWheelZoomPluginClass *klass)
{
}

static void
gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface)
{
	iface->activate = gedit_wheelzoom_plugin_app_activate;
	iface->deactivate = gedit_wheelzoom_plugin_app_deactivate;
}

static void
gedit_window_activatable_iface_init (GeditWindowActivatableInterface *iface)
{
	iface->activate = gedit_wheelzoom_plugin_window_activate;
	iface->deactivate = gedit_wheelzoom_plugin_window_deactivate;
	iface->update_state = gedit_wheelzoom_plugin_window_update_state;
}

G_MODULE_EXPORT void
peas_register_types (PeasObjectModule *module)
{
	gedit_wheelzoom_plugin_register_type (G_TYPE_MODULE (module));

	peas_object_module_register_extension_type (module,
						    GEDIT_TYPE_APP_ACTIVATABLE,
						    GEDIT_TYPE_WHEELZOOM_PLUGIN);
	peas_object_module_register_extension_type (module,
						    GEDIT_TYPE_WINDOW_ACTIVATABLE,
						    GEDIT_TYPE_WHEELZOOM_PLUGIN);
}

/* ex:set ts=8 noet: */
