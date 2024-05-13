const express = require('express');
const LoginController = require('../controllers/LoginController');
const AutoController = require('../controllers/AutoController');
const TopoController = require('../controllers/TopoController');
const OperaController = require('../controllers/OperaController')

const router = express.Router();

// Aquí incorporas las rutas para la carga de archivos YAML

router.get('/login', LoginController.login);
router.post('/login', LoginController.auth);
router.get('/update-admin', LoginController.showUpdateAdmin);  // Muestra la página de actualización para admin
router.post('/update-admin', LoginController.updateAdmin);
router.get('/register', LoginController.register);
router.post('/register', LoginController.printuser);
router.get('/logout', LoginController.logout);

//RUTAS PARA CONFIGURAR ARCHIVO YAML
router.get('/configure', AutoController.configure_ini);
router.post('/configure', AutoController.guardarDispositivo);
router.get('/upload', AutoController.configure_archivo);
router.post('/upload', AutoController.uploadYAML, AutoController.uploadYAMLFile);



//RUTA PARA VISUALIZAR TOPOLOGIA
router.get('/topologia', TopoController.topo_ini);

//RUTA PARA VISUALIZAR OPERACIONES

router.get('/operaciones', TopoController.operaciones_ini);

//RUTAS DENTRO DEL MODULO DE OPERACIONES

router.get('/snmp', OperaController.snmp);
router.post('/snmp', AutoController.guardarDispositivo);

router.get('/stp', OperaController.stp);
router.post('/stp', AutoController.guardarDispositivo);

router.get('/stp1', OperaController.stp1);
router.post('/stp1', AutoController.guardarDispositivo);

router.get('/vlan', OperaController.vlan);
router.post('/vlan', AutoController.guardarDispositivo);

router.get('/logs', OperaController.logs);
router.post('/logs', AutoController.guardarDispositivo);

module.exports = router;