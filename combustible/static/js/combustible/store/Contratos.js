Ext.define("ExtSiga.combustible.store.Contratos", {
	extend: "Ext.data.Store",
	model: "ExtSiga.combustible.model.Contrato",
	autoLoad: true,

	proxy: {
		type: "ajax",
		api: {
			create: "combustible/createContrato",
			read: "combustible/getContratosSiga",
			update: "combustible/createContrato",
			destroy: "combustible/deleteContrato"
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