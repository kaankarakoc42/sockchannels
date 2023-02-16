

// create a WebSocket object and connect to the server
const webSocket = new WebSocket('ws://localhost:1234');

// when the WebSocket connection is open
webSocket.addEventListener('open', () => {

  // send a message to the server
  webSocket.send(JSON.stringify({"channel":"join","user_id":"kaan12"}));
  setInterval(()=>{webSocket.send(JSON.stringify({"channel":"send_message","target":"kaan12","message":"selam"}))},1000)
});

// when the WebSocket receives a message
webSocket.addEventListener('message', (event) => {
  json = JSON.parse(event.data)
  console.log('Received data:',json );
  if(json.channel=="recv_messages"){
    element = document.getElementById("box");
    element.innerHTML = element.innerHTML + "<p>"+json.message+"</p>"
  }
});

// when the WebSocket connection is closed
webSocket.addEventListener('close', () => {
  console.log('WebSocket connection closed');
});