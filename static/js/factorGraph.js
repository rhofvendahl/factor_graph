
function Chat(){
  var self = this

  // create an array with nodes
  var nodes = new vis.DataSet([
    {id: 1, label: 'Node 1'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'}
  ]);

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 3, label: "causes", arrows: "to"},
    {from: 1, to: 2, label: "causes", arrows: "to"},
    {from: 2, to: 4, label: "causes", arrows: "to"},
    {from: 2, to: 5, label: "causes", arrows: "to"},
    {from: 3, to: 3, label: "causes", arrows: "to"}
  ]);

  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {};
  self.network = new vis.Network(container, data, options);

  self.log = document.getElementById('chat_log')
  self.input = document.getElementById('chat_input')
  self.socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
  self.session_id = Math.ceil(Math.random()*Math.pow(16, 8)).toString(16)
  const displacy = new displaCy('127.0.0.1:5000', {
    container: '#displacy',
    format: 'spacy',
    distance: 300,
    offsetX: 100
  });

  self.logMessage = function(content, sender){
    var msg_dom = document.createElement('div')
    msg_dom.innerHTML = content
    msg_dom.classList.add('msg', 'msg_' + sender)
    self.log.appendChild(msg_dom)
    self.log.scrollTop = self.log.scrollHeight;
  }

  self.input.onkeydown = function(event){
    if (event.key == 'Enter'){
      content = self.input.value
      self.logMessage(content, 'user')
      self.input.value = ''

      self.socket.emit('msg_user', {
        content: content,
        session_id: self.session_id
      });
    };
  };

  self.socket.on('msg_agent', function(msg){
    self.logMessage(msg.content, 'agent')

    if (msg.parse){
      displacy.render(msg.parse, {
        color: '#ff0000'
      });

      console.log(msg.parse);
      console.log(msg.nodes);
      console.log(msg.edges);

      self.network.setData({nodes: msg.nodes, edges: msg.edges})
    };
  });

}
