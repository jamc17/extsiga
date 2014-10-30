Ext.define("ExtSiga.combustible.model.Contrato", {
	extend: "Ext.data.Model",

	idProperty: "secContrato",

	fields: [
		{name: "secContrato", type: "string"},
		{name: "anoEje", type: "string"},
		// {name: "secEjec", type: "string"},
		{name: "tipoBien", type: "string"},
		{name: "nroDocumento", type: "string"},
		// {name: "glosa", type: "string"},
		// {name: "especTecnicas", type: "string"},
		{name: "proveedor", type: "string"},
	],

});