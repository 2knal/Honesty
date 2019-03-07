
// Initialise Pusher
const pusher = new Pusher('90a028630895e82ad6bc', {
    cluster: 'ap2',
    encrypted: true
});


function submit_message(message) {
    
    $.post( "/send_message", {
        message: message, 
        socketId: pusher.connection.socket_id
    }, handle_response);
    
    function handle_response(data) {
      // append the bot repsonse to the div
      a=data.message.replace("^","<a>");
      $('.chat-container').append(`
            <div class="chat-message col-md-9 offset-md-7 bot-message">
                ${a.split("%").join("<br>")}
            </div>
      `)
      // remove the loading indicator
      $( "#loading" ).remove();
    }
}


$('#target').on('submit', function(e){
    e.preventDefault();
    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }
    
    
    $('.chat-container').append(`
        <div class="chat-message col-md-5 human-message">
            ${input_message}
        </div>
    `)
    
    // loading 
    $('.chat-container').append(`
        <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
            <b>...</b>
        </div>
    `)
    
    // clear the text input 
    $('#input_message').val('')
    console.log(input_message)
    // send the message
    submit_message(input_message)
});


function openForm() {

    if (document.getElementById("myForm").style.display == "block") {
        document.getElementById("myForm").classList.remove('animated', 'zoomInUp')
        document.getElementById("myForm").classList.add('animated', 'zoomOutDown')
        sleep(500).then(() => {
            document.getElementById("myForm").style.display = "none";
        });

    } else {
        document.getElementById("myForm").style.display = "block";
        document.getElementById("myForm").classList.remove('animated', 'zoomOutDown');
        document.getElementById("myForm").classList.add('animated', 'zoomInUp');
    }
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

$(document).ready(function(){
    for( i = 1; i<= document.getElementsByClassName('card').length; i++)
    {
        console.log(document.getElementsByClassName('card')[i-1])
        document.getElementsByClassName('card')[i-1].id="btn" + i;
        document.getElementsByClassName('modal')[i-1].className += " "+"modal" + i;
    }

    $(".card").hover(function(){
        $(this).addClass("z-depth-2");
    }, function(){
        $(this).removeClass("z-depth-2");
    });

    $(".card").on("click", function(){
        console.log(this.id);
        number=this.id.replace("btn","");
        console.log(number)
        $(".modal"+number).addClass("show animated zoomIn" );
        $("#btn"+number).attr("data-target",".modal"+number)
    });
});


function closeModal()
{
    $(".modal"+number).addClass("animated zoomOut" );
}