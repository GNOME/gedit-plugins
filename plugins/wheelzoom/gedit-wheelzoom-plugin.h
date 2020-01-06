/*
 * gedit-wheelzoom-plugin.h
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

#ifndef GEDIT_WHEELZOOM_PLUGIN_H
#define GEDIT_WHEELZOOM_PLUGIN_H

#include <glib.h>
#include <glib-object.h>
#include <libpeas/peas-extension-base.h>
#include <libpeas/peas-object-module.h>

G_BEGIN_DECLS

#define GEDIT_TYPE_WHEELZOOM_PLUGIN			(gedit_wheelzoom_plugin_get_type ())
#define GEDIT_WHEELZOOM_PLUGIN(o)			(G_TYPE_CHECK_INSTANCE_CAST ((o), GEDIT_TYPE_WHEELZOOM_PLUGIN, GeditWheelZoomPlugin))
#define GEDIT_WHEELZOOM_PLUGIN_CLASS(k)		(G_TYPE_CHECK_CLASS_CAST((k), GEDIT_TYPE_WHEELZOOM_PLUGIN, GeditWheelZoomPluginClass))
#define GEDIT_IS_WHEELZOOM_PLUGIN(o)		(G_TYPE_CHECK_INSTANCE_TYPE ((o), GEDIT_TYPE_WHEELZOOM_PLUGIN))
#define GEDIT_IS_WHEELZOOM_PLUGIN_CLASS(k)	(G_TYPE_CHECK_CLASS_TYPE ((k), GEDIT_TYPE_WHEELZOOM_PLUGIN))
#define GEDIT_WHEELZOOM_PLUGIN_GET_CLASS(o)	(G_TYPE_INSTANCE_GET_CLASS ((o), GEDIT_TYPE_WHEELZOOM_PLUGIN, GeditWheelZoomPluginClass))

typedef struct _GeditWheelZoomPlugin		GeditWheelZoomPlugin;
typedef struct _GeditWheelZoomPluginPrivate	GeditWheelZoomPluginPrivate;
typedef struct _GeditWheelZoomPluginClass	GeditWheelZoomPluginClass;

struct _GeditWheelZoomPlugin
{
	PeasExtensionBase parent;

	/*< private >*/
	GeditWheelZoomPluginPrivate *priv;
};

struct _GeditWheelZoomPluginClass
{
	PeasExtensionBaseClass parent_class;
};

GType			gedit_wheelzoom_plugin_get_type	(void) G_GNUC_CONST;

G_MODULE_EXPORT void	peas_register_types		(PeasObjectModule *module);

G_END_DECLS

#endif /* GEDIT_WHEELZOOM_PLUGIN_H */
/* ex:set ts=8 noet: */
