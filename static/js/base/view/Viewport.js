Ext.define("ExtSiga.view.Viewport", {
	// require: ["Ext.container.Viewport"],
	extend: "Ext.container.Viewport",
	layout: "border",


	initComponent: function () {
		var me = this;

		me.items = [{
				xtype: "panel",
				region: "north",
				height: 80,
				loader: {
					// url: "/header",
					// autoLoad: true
				}

			}, {
				xtype: "panel",
				region: "west",
				title: "Menu Opciones",
				collapsible: true,
				split: true,
				flex: 1,
				// layout: "accordion",
				defaults: {
					xtype: 'treepanel',
					rootVisible: false,
					listeners: {
						itemdblclick: {
							fn: me.treeActions,
							scope: me
						}
					}
				},
				loader: {
					// autoLoad: true,
					// url: "/mainMenu",
					renderer: "component"
				},
			}, {
				itemId: "panelCentral",
				xtype: "panel",
				layout: "fit",
				region: "center",
				title: "EXTSIGA - Contenido",
				flex: 5,
				loader: {
					// url: "/center",
					// autoLoad: true
				}
			}, {
				xtype: "panel",
				region: "south",
				height: 50,
				loader: {
					// url: "/footer",
					// autoLoad: true
				}
			}
		];

		this.callParent();
	},

	treeActions: function (view, record, item, index, e, eOpts) {
		var viewport = this;
		var itemSel = record.get("qtitle");
		if (record.get("leaf")) {
			try {
				Ext.create("Gedacer.view." + itemSel, {
					viewport: viewport
				});
			} catch (Err) {
				console.log(Err);
			}
		}
	}

});