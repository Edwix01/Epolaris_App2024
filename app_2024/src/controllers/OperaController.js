function snmp(req, res) {
    if (req.session.loggedin ){
      res.render('epops/snmp', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

function stp(req, res) {
    if (req.session.loggedin ){
      res.render('epops/stp', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function stp1(req, res) {
    if (req.session.loggedin ){
      res.render('epops/stp1', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function vlan(req, res) {
    if (req.session.loggedin ){
      res.render('epops/vlan', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function logs(req, res) {
    if (req.session.loggedin ){
      res.render('epops/logs', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }
  
    module.exports = {
      snmp: snmp,
      stp:stp,
      vlan:vlan,
      stp1:stp1,
      logs:logs,
    }