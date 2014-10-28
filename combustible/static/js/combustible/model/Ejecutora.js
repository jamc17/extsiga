Ext.define("ExtSiga.combustible.model.Ejecutora", {
	extend: "Ext.data.Model",
	requires: ["ExtSiga.combustible.model.Contrato"],
	idProperty: "secEjec",
	fields: [
		{name: "secEjec"},
		{name: "nombre"},
		{name: "ruc"},
		{name: "localidad"},
		{name: "lugar"},
		{name: "lugarNum"}
	],
	validators: [
		{type: "presence", field: "secEjec"},
		{type: "presence", field: "nombre"},
		{type: "length", field: "ruc", min:11, max:11},
		{type: "format", field: "localidad", matcher: /^[\w ]+$/},
	],
	hasMany: [
		{model: "ExtSiga.combustible.model.Contrato", name: "getContratos"}
	]
});