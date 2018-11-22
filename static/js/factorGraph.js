function Chat(){
  var self = this
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
    }
  };

  self.socket.on('msg_agent', function(msg){
    self.logMessage(msg.content, 'agent')

    displacy.render(msg.parse, {
      color: '#ff0000'
    });
  });

}
