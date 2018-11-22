var channel = "/chat";

var socket = io.connect('http://' + document.domain + ':' + location.port + channel);

chat_history = {}

function new_chat(e) {
    var username = e.children[0].value;

    try {
        chatWith;
        history[chatWith] = document.getElementById("message_body").innerHTML;
    }
    catch(err) {
    }
    chatWith = username;
    $('.user').removeClass("active");
    e.classList.add("active");
    document.getElementById("message_head").classList.remove("hidden");
    document.getElementById('uname').innerHTML = username;
    
    if(history[chatWith] === undefined) {
        document.getElementById('message_body').innerHTML = "";
    } else {
        document.getElementById('message_body').innerHTML = history[chatWith];
    }
    document.getElementById('msg_to_send').value = "";
    document.getElementById("card_footer").style.display = "block";
}

socket.on('connect', function() {
    socket.emit('my_connection', {data: 'I\'m connected!'});
});

socket.on("message", function (message) {
    //alert("you got a msg");
    console.log('message arrived from ' + message.from);
    
    // either recieve msg from the person you are currently
    // chatting or someone else

    var new_message = ` <div class="d-flex justify-content-start mb-4">
                                <div class="msg_cotainer">
                                    ${message.message}
                                    <span class="msg_time">${message.time}</span>
                                </div>
                                <div class="img_cont_msg">
                                    <img src="/static/img/avatar.png" class="rounded-circle user_img_msg">
                                </div>
                            </div>`

    if(message.from == chatWith) {
        // text message from the user you are already chatting with
        document.getElementById('message_body').innerHTML += new_message;
    } else {
        // text message from someone else
        
        console.log("handle it as notification");
        if(history[message.from] === undefined) {
            history[message.from] = new_message;
        } else {
            history[message.from] += new_message;
        }

        //alert("chat recieved from " + message.from);
        swal({
            title: 'Incoming chat',
            text: "Received message from " + message.from,
            type: '',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Open Chat'
          }, function(result) {
            console.log(result);
            if (result) {
                var available_users = document.querySelectorAll("li");
                for(var i = 0; i < available_users.length; ++i) {
                    console.log(available_users[i].children[0].value)
                    if(available_users[i].children[0].value == message.from) {
                        console.log(available_users[i]);
                        new_chat(available_users[i]);
                        break;
                    }
                }
            }
          });
    }
    

    //refreshMessages(message['data']);
});

function refreshMessages(message) {
    $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
        + message.message + '<br/><small class="text-muted">' + message.author + ' | ' + message.createDate + '</small><hr/></div></div></div></li>');
}

$(document).ready(function() {
    $('#action_menu_btn').click(function(){
        $('.action_menu').toggle();
    });
});


function send_message() {
    var message = $("#msg_to_send")[0].value
    console.log(message);
    console.log(chatWith);
    var date = new Date()
    var meridian = "am";
    var hours = date.getHours();
    if(hours>12){
        hours -= 12;
        meridian = "pm";
    }
    var new_message = `<div class="d-flex justify-content-end mb-4">
        <div class="msg_cotainer_send">
            ${message}
            <span class="msg_time_send">${ hours + ":" + date.getMinutes()+meridian}</span>
        </div>
        <div class="img_cont_msg">
    <img src="/static/img/avatar.png" class="rounded-circle user_img_msg">
        </div>
    </div>`
    document.getElementById('message_body').innerHTML += new_message;
    
    socket.emit('message', {
                            to: chatWith, 
                            time: hours + ":" + date.getMinutes() + meridian, 
                            message: message    
                        })

    document.getElementById('msg_to_send').value = "";
    document.getElementById('results').innerHTML = "";

}

function update_contacts() {
    var login_xhr = new XMLHttpRequest();
    var logout_xhr = new XMLHttpRequest();
    
    console.log("new_login");
    console.log("update_logout");

    login_xhr.open("GET", "/new_login", true);
    logout_xhr.open("GET", "/update_logout", true);

    login_xhr.onreadystatechange = add_to_contacts;
    logout_xhr.onreadystatechange = remove_from_contacts;

    login_xhr.send();
    logout_xhr.send();
    function add_to_contacts() {
        if(this.status == 200 && this.readyState == 4) {
            var someone = this.responseText
            var all_contacts = document.getElementById("all_contacts");

            var new_contact = ` <li class="user" onclick="new_chat(this)">
                                    <input type="text" value=${someone} style="display:none">
                                    <div class="d-flex bd-highlight">
                                        <div class="img_cont">
                                            <img src="/static/img/avatar.png" class="rounded-circle user_img">
                                            <span class="online_icon"></span>
                                        </div>
                                        <div class="user_info">
                                            <span>${someone}</span>
                                            <p>${someone} is online</p>
                                        </div>
                                    </div>
                                </li>`

            all_contacts.innerHTML += new_contact;
            setTimeout(update_contacts, 2000);
        }
    }

    function remove_from_contacts() {
        if(this.status == 200 && this.readyState == 4) {
            var someone = this.responseText
            console.log(someone + " left");
            var all_contacts = document.getElementById("all_contacts");
            for(var i = 0; i < all_contacts.children.length; ++i) {
                if(all_contacts.children[i].children[0].value == someone) {
                    all_contacts.children[i].parentNode.removeChild(all_contacts.children[i]);
                    break;
                }
            }
            setTimeout(update_contacts, 2000);
        }    
    }
    
}