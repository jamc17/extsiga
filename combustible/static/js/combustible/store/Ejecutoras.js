Ext.define("ExtSiga.combustible.store.Ejecutoras", {
	extend: "Ext.data.Store",
	model: "ExtSiga.combustible.model.Ejecutora",
	autoLoad: true,

	proxy: {
		type: "ajax",
		api: {
			create: "combustible/createEjecutora",
			read: "combustible/getEjecutoras",
			update: "combustible/createEjecutora",
			destroy: "combustible/deleteEjecutora"
		},
		reader: {
			type: "json",
			root: "data"
		},
		writer: {
			type: "json",
			allowSingle: false
		}
	}
});