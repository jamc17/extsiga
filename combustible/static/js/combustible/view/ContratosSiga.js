Ext.define("ExtSiga.combustible.view.ContratosSiga", {
    singleton: true,
    config: {
        centerReg: null
    },

    statics : {
        instancia: null,
        sequence: 0,
        nextId: function () {
            return ++this.sequence;
        }
    },

    cargarMaestrosSiga: function (button, e) {
        Ext.Msg.confirm("Confirmar", "Desea realizar la importación de datos maestros desde el SIGA", function (res) {
            if (res == "yes") {
                
                Ext.Ajax.request({
                    url: "/combustible/importarContratosSiga",
                    timeout: 180000,
                    success: function (xhr) {
                        var res = Ext.decode(xhr.responseText);
                        if (res.estado) {
                            Ext.Msg.show({
                                title: "Mensaje",
                                msg: res.mensaje,
                                buttons: Ext.MessageBox.OK,
                                icon: Ext.MessageBox.INFO
                            });
                        }
                        else {
                            Ext.Msg.show({
                                title: "Error",
                                msg: res.mensaje,
                                buttons: Ext.MessageBox.OK,
                                icon: Ext.MessageBox.WARNING
                            });
                        }
                    },
                    failure: function (xhr) {
                        var msg = "Error en la carga de datos, contácte al administrador de sistemas!!!";

                        Ext.Msg.show({
                                title: "Error",
                                msg: msg,
                                buttons: Ext.MessageBox.OK,
                                icon: Ext.MessageBox.ERROR
                            });
                    }
                });
            }
        });
    },

    initComponents: function () {
        var me = this;
        this.filtros = Ext.create("Ext.Component", {
            region: "north",
            height: 60,
            loader: {
                url: "combustible/filtrosContratosSiga",
                autoLoad: true
            },
            style: {
                backgroundColor: "white"
            }
        });

        this.gridContratos = Ext.create("Ext.grid.Panel", {
            title: "Contratos SIGA",
            region: "center",
            header: {
                defaults: {
                    xtype: "button",
                    style: {
                        marginRight: "5px"
                    }
                },
                items: [
                {
                    cls: "buttonWarnning",
                    focusCls: "buttonWarnning",
                    text: "Importar maestros del SIGA",
                    handler: me.cargarMaestrosSiga
                }]
            },
            store: Ext.create("ExtSiga.combustible.store.Contratos"),
            columns: [
                {xtype: 'rownumberer', width: 40},
                {text: "Nro Contrato", dataIndex: "nroDocumento", flex: 3},
                {text: "Proveedor", dataIndex: "proveedor", flex: 6},
                {text: "Acciones", renderer: function (value, metaData, record) {
                    metaData.style = "text-align: center";
                    return "<a href='#' class='button'>Agregar</a>";
                }}
            ],
            bodyCls: "gridMayusculas",
            listeners: {
                rowdblclick: {
                    fn: me.getDetalleContratoSiga,
                    scope: me
                }
            }
        });
        
        this.panelDetalleContrato = Ext.create("Ext.Component", {
            region: "north",
            split: true,
            loader: {
                url: "combustible/getDetalleContratoSiga",
                autoLoad: true
            },
        });
        
    },

    getDetalleContratoSiga: function (table, record) {
        var idContrato = record.get("secContrato");

        this.panelDetalleContrato.getLoader().load(
            {
                params: {secContrato: idContrato},
                method: "GET"
            });
    },

    renderizate: function (config) {
        var me = this;
        // var oldCmp = this.self.centerReg.removeAll(true);
        // oldCmp = null;
        if (!me.self.instancia) {
            me.initConfig(config);

            //Configuramos la variable de clase para obtener el singleton
            me.self.instancia = me;
            
            //Inicializamos los componentes
            this.initComponents();

            me.getCenterReg().add([
            {
                xtype: "container",
                layout: {
                    type: "border",
                },
                defaults: {
                    xtype: "panel",
                    flex: 1,
                    border: false
                },
                items: [
                    {
                        region: "west",
                        split: true,
                        layout: {
                            type: "border"
                        },
                        items: [me.filtros, me.gridContratos]
                    }, {
                        region: "center",
                        layout: "border",
                        defaults: {
                            xtype: "component",
                            border: '0 0 1 0',
                            flex: 1,
                            style: {
                                backgroundColor: "white",
                                borderColor: "#ccc",
                                borderStyle: "solid",
                            }

                        },
                        items: [me.panelDetalleContrato, {
                            region: "center",
                            html: "Listado contratos seleccionados"
                        }]
                    }]
            }]);
        } else {
            this.reloadPanels();
        }
        
    },

    reloadPanels: function () {
        this.filtros.getLoader().load();
        this.gridContratos.store.load();
        this.panelDetalleContrato.getLoader().load();
    }
});