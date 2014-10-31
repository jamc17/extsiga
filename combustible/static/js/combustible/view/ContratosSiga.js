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

    cargarMaestrosSiga: function (meObj) {
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

                            //Actializamos el store de contratos siga
                            meObj.gridContratos.getStore().load();
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
                autoLoad: true,
                callback: function () {
                    // Configuramos los listeners
                    var listas = Ext.select("#formFiltrosContratosSiga select");
                    listas.each(function (lista) {
                        Ext.get(lista).on("change", me.filtrarContrtosSiga, me);
                    });
                }
            },
            style: {
                backgroundColor: "white"
            }
        });

        storeContratos = Ext.create("ExtSiga.combustible.store.Contratos");

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
                    handler: function () {
                        me.cargarMaestrosSiga(me);
                    }
                }]
            },
            store: storeContratos,
            columns: [
                {xtype: 'rownumberer', width: 30},
                {text: "Nro Contrato", dataIndex: "nroDocumento", flex: 3},
                {text: "Proveedor", dataIndex: "proveedor", flex: 7},
                {
                    xtype: "actioncolumn",
                    width: 30,
                    items: [
                    {
                        xtype: "button",
                        tooltip: "Agregar",
                        icon: "static/img/add-icon-small.png",
                        handler: function (grid, rowIndex) {
                            me.selecContrato(grid, rowIndex)
                        }
                        
                    }]
                }
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


        storeContratosLocal = Ext.create("ExtSiga.combustible.store.Contratos");
        storeContratosLocal.setProxy({
            type: "localstorage",
            id: "extsiga"
        });
        
        // me.gridContratos.getStore().onAfter("load", function (store) {
        //     contratosSel = storeContratosLocal.getData().items;
            
        //     store.remove(contratosSel);
        // });

        this.gridContratosSel = Ext.create("Ext.grid.Panel", {
            title: "Contratos Seleccionados",
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
                    text: "Limpiar",
                    handler: function () {
                        me.limpiarContratosSeleccionados(me);
                    }
                }, {
                    text: "Guardar",
                    handler: function () {
                        me.guardarContratosCombustible(me);
                    }
                }]
            },
            store: storeContratosLocal,
            columns: [
                {xtype: 'rownumberer', width: 30},
                {text: "Nro Contrato", dataIndex: "nroDocumento", flex: 3},
                {text: "Proveedor", dataIndex: "proveedor", flex: 7},
                {
                    xtype: "actioncolumn",
                    width: 30,
                    items: [
                    {
                        xtype: "button",
                        tooltip: "Quitar",
                        icon: "static/img/delete-icon-small.png",
                        handler: function (grid, rowIndex) {
                            me.quitContrato(grid, rowIndex)
                        }
                    }]
                }
            ],
            bodyCls: "gridMayusculas",
            listeners: {
                rowdblclick: {
                    fn: me.getDetalleContratoSiga,
                    scope: me
                }
            }
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
                            flex: 1,
                            style: {
                                backgroundColor: "white",
                            }
                        },
                        items: [me.panelDetalleContrato, me.gridContratosSel]
                    }]
            }]);
        } else {
            this.reloadPanels();
        }
    },

    getDetalleContratoSiga: function (table, record) {
        var idContrato = record.get("secContrato");

        this.panelDetalleContrato.getLoader().load(
            {
                params: {secContrato: idContrato},
                method: "GET"
            });
    },

    selecContrato: function (grid, rowIndex) {
        var rec = grid.getStore().getAt(rowIndex);
        var storeContratosSelec = this.gridContratosSel.getStore();
        
        storeContratosSelec.add(rec);
        grid.getStore().remove(rec)
        
        // Persistimos la data en el LocalStorage :)
        rec.set("id", null);
        storeContratosSelec.sync();
    },

    quitContrato: function (grid, rowIndex) {
        var rec = grid.getStore().getAt(rowIndex);
        grid.getStore().remove(rec);
        this.gridContratos.getStore().insert(0, rec);

        grid.getStore().sync();
    },

    limpiarContratosSeleccionados: function(meObj) {
        var storeCont = meObj.gridContratos.getStore();
        var storeContSel = meObj.gridContratosSel.getStore();
        var contratosSel = storeContSel.removeAll();
        storeCont.insert(0, contratosSel);

        storeContSel.sync();
    },

    guardarContratosCombustible: function (meObj) {
        var store = meObj.gridContratosSel.getStore();
        var data = {contratos: []};
        
        if (store.count()) {
            store.each(function (record) {
                data.contratos.push(record.get("secContrato"));
            });
            // console.log(data);

            Ext.Msg.confirm("Confirmar", "Desea generar los contratos SIGA", function (res) {
                if (res == "yes") {
                    Ext.Ajax.request({
                        url: "/combustible/guardarContratosCombustible",
                        jsonData: data,
                        success: function (xhr) {
                            var res = Ext.decode(xhr.responseText);
                            if (res.estado) {
                                Ext.Msg.show({
                                    title: "Mensaje",
                                    msg: res.mensaje,
                                    buttons: Ext.MessageBox.OK,
                                    icon: Ext.MessageBox.INFO
                                });

                                // Limpiamos el store y sincronizamos con el localstorage
                                store.removeAll();
                                store.sync();

                                meObj.gridContratos.getStore().load();
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
                            var msg = "Error al generar los contratos de combustible, contácte al administrador de sistemas!!!";

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
        } else {
            var msg = "No existen contratos para procesar, por favor seleccione al menos un contrato.";

            Ext.Msg.show({
                title: "Error",
                msg: msg,
                buttons: Ext.MessageBox.OK,
                icon: Ext.MessageBox.WARNING
            });
        }
    },

    filtrarContrtosSiga: function () {
        me = this;
        var formFilters = Ext.get("formFiltrosContratosSiga");
        var storeContratos = me.gridContratos.getStore();
        storeContratos.getProxy().setExtraParams(
            {tipoBien: Ext.get("tipoBien").getValue(), anoEje: Ext.get("year").getValue()}
        );
        // console.log(Ext.get("tipoBien").getValue(), Ext.get("year").getValue());
        storeContratos.load();
    },

    reloadPanels: function () {
        this.filtros.getLoader().load();
        this.gridContratos.getStore().getProxy().setExtraParams({});
        this.gridContratos.store.load();
        this.gridContratosSel.store.load();
        this.panelDetalleContrato.getLoader().load();
    }
});