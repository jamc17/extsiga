Ext.define("ExtSiga.combustible.model.Contrato", {
	extend: "Ext.data.Model",

	idProperty: "secContrato",

	fields: [
		{name: "secContrato", type: "string"},
		{name: "anoEje", type: "string"},
		{name: "secEjec", type: "string"},
		{name: "tipoBien", type: "string"},
		{name: "nroDocumento", type: "string"},
		{name: "proveedor", type: "int", mapping:"proveedor_id"},
		{name: "glosa", type: "string"},
		{name: "especTecnicas", type: "string"},
	]
});