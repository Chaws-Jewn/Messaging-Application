# Messaging-Application
Messaging application using sockets, tkinter, and threading
<pre>
SERVER SIDE:
Added start_server() to store how to start server.
Support ipv4 and tcp client connection

Added a indefinite loop for accepting clients via accept_client(server)
In accept_client we passed server as args

Created a loop for accepting the client, collect data (username and socket):
Add a response to be sent to the user
  If there is already a connected client, loop through saved clients; check if the collected username for the new client is already saved to another user
  If client list is empty or there is no match for the username, add the user to the chat room; else disconnect the client, allow for another entry of username

Add an indefinite loop of receiving message:
  Accept the client information as args
  Loop to check the name of the username of the client
  Add the username of the sender to the message and the message itself
  Print the message to server call the send_message_to_clients function

Add catching for disconnected users:
  Catch the error and proceed
  Identify user details
  Add message/notification that user has disconnected
  Delete user details

send_message_to_clients function
  loop through the saved clients
  for each client, send the message
  
________________________________________________________________________________
  
CLIENT SIDE:
Create and configure the ui
Disable messaging entry and button
Enable input for username, collect entry and send to server
Upon clicking join chat, disable username entry and button
Connect to server and wait for response
If sent response is 'failed', a prompt would appear then create another username and try to connect again; else continue to program
Upon entry, message area and messaging would be enabled, together with "Enter" bind for sending

send_message function:
  Get the message entry value, encode, and send to server
  Reset the message entry

Messages would be sent by server and displayed on message area
</pre>
