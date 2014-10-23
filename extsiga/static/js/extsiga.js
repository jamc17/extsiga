// Ext.require("ExtSiga.view.Viewport");
Ext.onReady(function () {
	
	viewport = Ext.create("ExtSiga.base.view.Viewport", {
        renderTo: Ext.getBody()
    });

    // Se puede mejorar
    // Defino mascaras al viewport para todas las peticiones ajax
    Ext.Ajax.on("beforerequest", function(){
        viewport.mask("Cargando");
    });
    Ext.Ajax.on("requestcomplete", function(){
        viewport.unmask();
    });
	
});
